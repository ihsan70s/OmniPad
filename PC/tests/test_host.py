import unittest
import asyncio
from aiohttp.test_utils import TestServer, TestClient
from server import Input, validate, make_app

class Validation(unittest.TestCase):
    def test_reject(self):
        for p in [{'type':'move','dx':float('nan'),'dy':0},{'type':'key','name':'shutdown','down':True},{'type':'button','name':'left','down':'true'},{'type':'text','text':'x'*201},{'type':'shell'},[]]:
            with self.assertRaises(ValueError): validate(p)
    def test_full_controller_mapping_and_reset(self):
        adapter=Input()
        for key in ['w','a','s','d','up','down','left','right','i','j','l','space','q','z','e','c','shift','k','tab','enter','home']:
            adapter.perform({'type':'key','name':key,'down':True})
        self.assertEqual(len(adapter.held),21)
        adapter.release()
        self.assertFalse(adapter.held)
    def test_keyboard_shortcut_and_punctuation(self):
        adapter=Input()
        for key in ['ctrl','alt','cmd','shift','delete','f12','7','?',"'",']']:
            adapter.perform({'type':'key','name':key,'down':True})
        adapter.release()
        self.assertFalse(adapter.held)
    def test_keyboard_rejects_unlisted_control_names(self):
        for key in ['shutdown','launch_app','ctrl+c','unknown_key','\\n']:
            with self.assertRaises(ValueError):
                validate({'type':'key','name':key,'down':True})
    def test_release_idempotent(self):
        a=Input();a.perform({'type':'key','name':'w','down':True});a.perform({'type':'key','name':'w','down':True})
        self.assertEqual(a.events,1);a.release();a.release();self.assertEqual(a.held,set());self.assertEqual(a.events,2)
class SocketTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.a=Input();self.client=TestClient(TestServer(make_app(self.a,'test-secret')));await self.client.start_server()
        self.origin=str(self.client.make_url('/')).rstrip('/')
    async def asyncTearDown(self): await self.client.close()
    async def connect(self,token='test-secret'):
        w=await self.client.ws_connect('/ws',headers={'Origin':self.origin});await w.send_json({'token':token});return w,await w.receive_json()
    async def test_auth(self):
        w,m=await self.connect('wrong');self.assertEqual(m['error'],'unauthorized');await w.close()
    async def test_origin(self):
        from aiohttp import WSServerHandshakeError
        with self.assertRaises(WSServerHandshakeError):await self.client.ws_connect('/ws',headers={'Origin':'http://evil.example'})
    async def test_exclusive_and_release(self):
        w,m=await self.connect();self.assertEqual(m['type'],'ready')
        other,m=await self.connect();self.assertEqual(m['error'],'busy');await other.close()
        await w.send_json({'type':'key','name':'w','down':True});await w.receive_json();self.assertTrue(self.a.held)
        await w.close();await asyncio.sleep(.05);self.assertFalse(self.a.held)
    async def test_invalid_releases(self):
        w,_=await self.connect();await w.send_json({'type':'key','name':'a','down':True});await w.receive_json()
        await w.send_json({'type':'shell'});self.assertIn('error',await w.receive_json());await w.close();await asyncio.sleep(.05);self.assertFalse(self.a.held)
    async def test_shortcut_sequence_then_disconnect(self):
        w,_=await self.connect()
        for key,down in [('ctrl',True),('c',True),('c',False)]:
            await w.send_json({'type':'key','name':key,'down':down})
            self.assertEqual((await w.receive_json())['type'],'ack')
        self.assertEqual(self.a.held,{('key','ctrl')})
        await w.close();await asyncio.sleep(.05)
        self.assertFalse(self.a.held)
    async def test_watchdog(self):
        w,_=await self.connect();await w.send_json({'type':'key','name':'w','down':True});await w.receive_json()
        await asyncio.sleep(3.2);self.assertFalse(self.a.held);await w.close()
if __name__=='__main__':unittest.main()
