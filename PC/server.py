"""OmniPad LAN prototype. No shell commands or arbitrary key names accepted."""
import argparse
import asyncio
import json
import math
import secrets
import socket
import ssl
import time
import string
from pathlib import Path
from aiohttp import web, WSMsgType

ROOT = Path(__file__).parent
KEYS = {'home','i','j','k','l','q','e','z','c','tab','shift','w','a','s','d','space','enter','esc','left','right','up','down','backspace','f','media_play_pause','media_next','media_previous','media_volume_up','media_volume_down','media_volume_mute'}
KEYS |= set(string.ascii_letters + string.digits + string.punctuation)
KEYS |= {'ctrl','alt','cmd','delete','end','page_up','page_down','insert'} | {f'f{i}' for i in range(1,13)}
BUTTONS = {'left','right','middle'}

class Input:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.held = set()
        self.events = 0
        if not dry_run:
            from pynput import mouse, keyboard
            self.mouse, self.keyboard = mouse.Controller(), keyboard.Controller()
            self.Button, self.Key = mouse.Button, keyboard.Key
    def key(self, name):
        return getattr(self.Key, name) if len(name) > 1 else name
    def release(self):
        for kind, name in list(self.held):
            try:
                self.perform({'type':kind,'name':name,'down':False})
            except Exception:
                pass
        self.held.clear()
    def perform(self, p):
        validate(p)
        t = p['type']
        if t in {'key','button'}:
            item = (t,p['name'])
            if (item in self.held) == p['down']:
                return
            if p['down']: self.held.add(item)
            else: self.held.discard(item)
        self.events += 1
        if self.dry_run: return
        if t == 'move': self.mouse.move(round(p['dx']), round(p['dy']))
        elif t == 'scroll': self.mouse.scroll(0, round(p['dy']))
        elif t == 'text': self.keyboard.type(p['text'])
        elif t in {'key','button'}:
            device = self.keyboard if t == 'key' else self.mouse
            code = self.key(p['name']) if t == 'key' else getattr(self.Button,p['name'])
            (device.press if p['down'] else device.release)(code)

def validate(p):
    if not isinstance(p, dict): raise ValueError('object_required')
    t = p.get('type')
    if t in {'move','scroll'}:
        for name in (['dx','dy'] if t == 'move' else ['dy']):
            v = p.get(name)
            if type(v) not in (int,float) or not math.isfinite(v) or abs(v) > (500 if t == 'move' else 20):
                raise ValueError('invalid_delta')
    elif t in {'key','button'}:
        if p.get('name') not in (KEYS if t == 'key' else BUTTONS) or type(p.get('down')) is not bool:
            raise ValueError('invalid_input')
    elif t == 'text':
        if not isinstance(p.get('text'),str) or not 1 <= len(p['text']) <= 200:
            raise ValueError('invalid_text')
        if any(ord(c)<32 and c not in '\n\t' for c in p['text']): raise ValueError('control_character')
    else: raise ValueError('unknown_type')

def make_app(adapter=None, token=None, mirror_enabled=False, capture_factory=None, mirror_fps=15, mirror_width=1280, monitor_provider=None, default_monitor=1):
    adapter = adapter or Input()
    token = token or secrets.token_urlsafe(24)
    app = web.Application(client_max_size=4096)
    state = {'active':None, 'attempts':{}, 'sockets':set(), 'mirrors':set()}
    async def page(request):
        return web.FileResponse(ROOT/'web'/'index.html', headers={'Cache-Control':'no-store','Referrer-Policy':'no-referrer','X-Frame-Options':'DENY','Content-Security-Policy':"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' ws: wss:; frame-ancestors 'none'"})
    async def ws_handler(request):
        scheme = 'https' if request.secure else 'http'
        if request.headers.get('Origin') != f'{scheme}://{request.host}':
            raise web.HTTPForbidden(text='origin_rejected')
        ip = request.remote
        now = time.monotonic()
        attempts = [v for v in state['attempts'].get(ip,[]) if now-v<60]
        if len(attempts)>=10: raise web.HTTPTooManyRequests()
        attempts.append(now); state['attempts'][ip]=attempts
        # Bound pre-auth sockets; client data never selects a shell or executable.
        if len(state['sockets'])>=8: raise web.HTTPServiceUnavailable()
        ws = web.WebSocketResponse(max_msg_size=65536, heartbeat=2, compress=False)
        await ws.prepare(request)
        state['sockets'].add(ws)
        owns = False
        mirror = None
        try:
            msg = await asyncio.wait_for(ws.receive(),5)
            p = json.loads(msg.data)
            if not isinstance(p,dict) or not secrets.compare_digest(str(p.get('token','')),token):
                await ws.send_json({'error':'unauthorized'}); return ws
            if state['active'] is not None:
                await ws.send_json({'error':'busy'}); return ws
            state['active'] = ws; owns=True
            if mirror_enabled:
                from screen_stream import ScreenSession
                mirror = ScreenSession(ws.send_json, capture_factory, mirror_fps, mirror_width)
                state['mirrors'].add(mirror)
            await ws.send_json({'type':'ready','dry_run':adapter.dry_run,'protocol':1,'mirror':mirror_enabled,'default_monitor':default_monitor})
            count=0; window=time.monotonic()
            while True:
                msg = await asyncio.wait_for(ws.receive(),3)
                if msg.type != WSMsgType.TEXT: break
                p = json.loads(msg.data)
                if not isinstance(p,dict): raise ValueError('object_required')
                if p.get('type') != 'mirror_start' and len(msg.data.encode('utf-8')) > 4096: raise ValueError('message_too_large')
                now=time.monotonic()
                if now-window>=1: count=0; window=now
                count+=1
                if count>240: raise ValueError('rate_limited')
                if p.get('type')=='ping':
                    await ws.send_json({'type':'pong','id':p.get('id')})
                elif p.get('type')=='release': adapter.release()
                elif p.get('type')=='mirror_monitors':
                    if mirror is not None:
                        try:
                            from screen_stream import list_monitors
                            monitors = await asyncio.to_thread(monitor_provider or list_monitors)
                            await ws.send_json({'type':'mirror_monitors','monitors':monitors,'default_monitor':default_monitor})
                        except Exception:
                            await ws.send_json({'type':'mirror_monitors','monitors':[],'error':'unavailable'})
                elif p.get('type')=='mirror_start':
                    if mirror is None:
                        await ws.send_json({'type':'mirror_error','id':p.get('id'),'reason':'disabled'})
                    else:
                        await mirror.start(p.get('sdp'),p.get('id'),p.get('monitor'))
                elif p.get('type')=='mirror_stop':
                    if mirror is not None: await mirror.stop()
                else:
                    adapter.perform(p)
                    await ws.send_json({'type':'ack','events':adapter.events})
        except (ValueError,TypeError,asyncio.TimeoutError):
            if not ws.closed: await ws.send_json({'error':'invalid_or_timed_out'})
        except Exception:
            if not ws.closed: await ws.send_json({'error':'input_backend_failed'})
        finally:
            if owns:
                adapter.release(); state['active']=None
            if mirror is not None:
                await mirror.stop()
                state['mirrors'].discard(mirror)
            state['sockets'].discard(ws)
            await ws.close()
        return ws
    async def shutdown(app):
        adapter.release()
        for mirror in list(state['mirrors']): await mirror.stop()
        for ws in list(state['sockets']): await ws.close()
    app.router.add_get('/',page)
    app.router.add_get('/ws',ws_handler)
    app.on_shutdown.append(shutdown)
    return app

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--live',action='store_true',help='Enable OS mouse and keyboard control')
    p.add_argument('--host',default='0.0.0.0'); p.add_argument('--port',type=int,default=8765)
    p.add_argument('--ip',help='LAN IP advertised in QR; use ipconfig to select')
    p.add_argument('--cert'); p.add_argument('--key')
    p.add_argument('--mirror',action='store_true',help='Allow the paired phone to start desktop video')
    p.add_argument('--monitor',type=int,default=1,help='MSS monitor index, starting from 1')
    p.add_argument('--mirror-fps',type=int,choices=[5,10,15,20,30],default=15)
    p.add_argument('--mirror-width',type=int,choices=[640,960,1280],default=1280)
    a=p.parse_args()
    if a.monitor < 1: p.error('--monitor must be at least 1')
    capture_factory=None
    if a.mirror:
        from screen_stream import DesktopCapture
        capture_factory=lambda:DesktopCapture(a.monitor)
        print('Screen sharing enabled for monitor',a.monitor,'— starts only when the phone requests it.')
    token=secrets.token_urlsafe(24)
    ip=a.ip
    if not ip:
        try:
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as s:
                s.connect(('192.0.2.1',80)); ip=s.getsockname()[0]
        except OSError: ip='127.0.0.1'
    ctx=None
    if a.cert or a.key:
        if not (a.cert and a.key): p.error('--cert and --key must be supplied together')
        ctx=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER); ctx.load_cert_chain(a.cert,a.key)
    url=f"{'https' if ctx else 'http'}://{ip}:{a.port}/#{token}"
    print('\nOMNIPAD — '+('LIVE INPUT' if a.live else 'DRY RUN: no OS input'))
    print('Open on phone (same private Wi-Fi): '+url)
    print('Pairing link grants control. Stop/restart to revoke. Ctrl+C stops host.')
    try:
        import qrcode
        qr=qrcode.QRCode(); qr.add_data(url); qr.print_ascii(invert=True)
    except ImportError: print('QR unavailable; use link above.')
    web.run_app(make_app(Input(not a.live),token,mirror_enabled=a.mirror,capture_factory=capture_factory,mirror_fps=a.mirror_fps,mirror_width=a.mirror_width, default_monitor=a.monitor),host=a.host,port=a.port,ssl_context=ctx,access_log=None)
