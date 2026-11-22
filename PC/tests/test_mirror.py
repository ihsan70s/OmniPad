import asyncio
import unittest
from unittest.mock import patch
from PIL import Image
from aiohttp.test_utils import TestClient, TestServer
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription
from server import make_app, Input


class SyntheticCapture:
    def __init__(self):
        self.frames = 0
        self.closed = False
    def frame(self):
        self.frames += 1
        return Image.new('RGB', (320, 180), (20, 106, 184))
    def close(self):
        self.closed = True


class MirrorTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Integration fixture: use real UDP/DTLS/RTP on loopback, no OS interface enumeration.
        self.address_patch = patch('aioice.ice.get_host_addresses', return_value=['127.0.0.1'])
        self.address_patch.start()
        self.addCleanup(self.address_patch.stop)
        self.captures = []
        self.adapter = Input()
        def factory():
            c = SyntheticCapture(); self.captures.append(c); return c
        self.client = TestClient(TestServer(make_app(self.adapter, 'mirror-secret', mirror_enabled=True, capture_factory=factory, mirror_fps=5, mirror_width=640)))
        await self.client.start_server()
        self.origin = str(self.client.make_url('/')).rstrip('/')
        self.pc = None
        self.heartbeat = None
    async def asyncTearDown(self):
        if self.heartbeat:
            self.heartbeat.cancel()
            await asyncio.gather(self.heartbeat, return_exceptions=True)
        if self.pc:
            await self.pc.close()
        await self.client.close()
    async def connect(self, token='mirror-secret'):
        ws = await self.client.ws_connect('/ws', headers={'Origin':self.origin})
        await ws.send_json({'token':token})
        return ws, await ws.receive_json()
    async def receive_type(self, ws, kind):
        for _ in range(50):
            p = await asyncio.wait_for(ws.receive_json(), 10)
            if p.get('type') == kind: return p
            if p.get('type') == 'mirror_error': self.fail(str(p))
        self.fail('message not received')
    async def test_no_capture_before_explicit_start(self):
        ws, ready = await self.connect()
        self.assertTrue(ready['mirror'])
        self.assertFalse(self.captures)
        await ws.close()
        self.assertFalse(self.captures)
    async def test_unauthorized_cannot_start_capture(self):
        ws, message = await self.connect('wrong')
        self.assertEqual(message['error'],'unauthorized')
        self.assertFalse(self.captures)
        await ws.close()
    async def test_disabled_host_rejects_mirror(self):
        client = TestClient(TestServer(make_app(Input(),'disabled')))
        await client.start_server()
        try:
            origin = str(client.make_url('/')).rstrip('/')
            ws=await client.ws_connect('/ws',headers={'Origin':origin})
            await ws.send_json({'token':'disabled'})
            self.assertFalse((await ws.receive_json())['mirror'])
            await ws.send_json({'type':'mirror_start','id':1,'sdp':'m=video'})
            self.assertEqual((await ws.receive_json())['reason'],'disabled')
            await ws.close()
        finally: await client.close()
    async def test_video_end_to_end_and_stop_without_releasing_keyboard(self):
        ws,_ = await self.connect()
        async def heartbeat():
            while True:
                await ws.send_json({'type':'ping','id':0})
                await asyncio.sleep(.4)
        self.heartbeat = asyncio.create_task(heartbeat())
        self.pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))
        incoming = asyncio.get_running_loop().create_future()
        @self.pc.on('track')
        def on_track(track):
            if not incoming.done(): incoming.set_result(track)
        self.pc.addTransceiver('video', direction='recvonly')
        await self.pc.setLocalDescription(await self.pc.createOffer())
        await ws.send_json({'type':'mirror_start','id':1,'sdp':self.pc.localDescription.sdp})
        await ws.send_json({'type':'key','name':'ctrl','down':True})
        answer = await self.receive_type(ws,'mirror_answer')
        self.assertEqual(answer['id'],1)
        await self.pc.setRemoteDescription(RTCSessionDescription(sdp=answer['sdp'],type='answer'))
        track = await asyncio.wait_for(incoming,5)
        frame = await asyncio.wait_for(track.recv(),10)
        self.assertEqual((frame.width,frame.height),(320,180))
        self.assertGreaterEqual(self.captures[0].frames,2)
        self.assertIn(('key','ctrl'),self.adapter.held)
        await ws.send_json({'type':'mirror_stop'})
        await ws.send_json({'type':'ping','id':123})
        while (await self.receive_type(ws,'pong')).get('id') != 123: pass
        self.assertTrue(self.captures[0].closed)
        self.assertIn(('key','ctrl'),self.adapter.held)
        count = self.captures[0].frames
        await asyncio.sleep(.25)
        self.assertEqual(self.captures[0].frames,count)
        self.heartbeat.cancel();await asyncio.gather(self.heartbeat,return_exceptions=True);self.heartbeat=None
        await ws.close();await asyncio.sleep(.05)
        self.assertFalse(self.adapter.held)
    async def test_disconnect_closes_negotiated_capture(self):
        ws,_=await self.connect()
        self.pc=RTCPeerConnection(RTCConfiguration(iceServers=[]))
        self.pc.addTransceiver('video',direction='recvonly')
        await self.pc.setLocalDescription(await self.pc.createOffer())
        await ws.send_json({'type':'mirror_start','id':1,'sdp':self.pc.localDescription.sdp})
        await self.receive_type(ws,'mirror_answer')
        self.assertFalse(self.captures[0].closed)
        await ws.close()
        for _ in range(100):
            if self.captures[0].closed: break
            await asyncio.sleep(.01)
        self.assertTrue(self.captures[0].closed)
    async def test_capture_failure_reports_and_closes(self):
        class Broken(SyntheticCapture):
            def frame(self): raise RuntimeError('no desktop')
        from screen_stream import ScreenSession
        messages=[];capture=Broken()
        async def emit(p): messages.append(p)
        session=ScreenSession(emit,lambda:capture)
        await session.start('m=video',1)
        task=session.task
        await asyncio.wait_for(task,3)
        self.assertEqual(messages[0]['type'],'mirror_error')
        self.assertTrue(capture.closed)
        await session.stop()
    async def test_invalid_offer_rejected_without_capture(self):
        ws,_=await self.connect()
        await ws.send_json({'type':'mirror_start','id':1,'sdp':'not a video offer'})
        self.assertIn('error',await ws.receive_json())
        await ws.close()
        self.assertFalse(self.captures)

    async def test_monitor_inventory_without_capture(self):
        ws, _ = await self.connect()
        monitors = [{'id':1,'width':1920,'height':1080,'left':0,'top':0}, {'id':2,'width':1280,'height':1024,'left':-1280,'top':0}]
        with patch('screen_stream.list_monitors', return_value=monitors):
            await ws.send_json({'type':'mirror_monitors'})
            message = await ws.receive_json()
        self.assertEqual(message['monitors'], monitors)
        self.assertFalse(self.captures)
        await ws.close()

    async def test_selected_monitor_reaches_capture(self):
        from screen_stream import ScreenSession
        capture = SyntheticCapture()
        session = ScreenSession(lambda p: asyncio.sleep(0), lambda: capture)
        pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))
        try:
            pc.addTransceiver('video', direction='recvonly')
            await pc.setLocalDescription(await pc.createOffer())
            await session.start(pc.localDescription.sdp, 1, monitor=2)
            await asyncio.wait_for(session.task, 5)
            self.assertEqual(capture.monitor, 2)
        finally:
            await session.stop()
            await pc.close()
        self.assertTrue(capture.closed)

    async def test_invalid_monitor_does_not_capture(self):
        from screen_stream import ScreenSession
        session = ScreenSession(lambda p: asyncio.sleep(0), lambda: self.fail('must not capture'))
        for monitor in [0, -1, True, '2', 257]:
            with self.assertRaises(ValueError):
                await session.start('m=video', 1, monitor=monitor)
