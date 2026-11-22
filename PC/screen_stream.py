"""Opt-in desktop-to-browser WebRTC video. No files or audio are recorded."""
import asyncio
import fractions
import time
from concurrent.futures import ThreadPoolExecutor
from aiortc import RTCConfiguration, RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.mediastreams import MediaStreamError
from av import VideoFrame


def list_monitors():
    import mss
    with mss.mss() as screen:
        return [dict(id=i, width=m['width'], height=m['height'], left=m['left'], top=m['top'])
                for i, m in enumerate(screen.monitors) if i > 0]


class DesktopCapture:
    """All methods run on one capture thread (MSS contexts are thread-local)."""
    def __init__(self, monitor=1):
        self.monitor = monitor
        self.screen = None

    def frame(self):
        import mss
        from PIL import Image
        if self.screen is None:
            self.screen = mss.mss(with_cursor=True)
        if not 1 <= self.monitor < len(self.screen.monitors):
            raise ValueError('monitor_unavailable')
        shot = self.screen.grab(self.screen.monitors[self.monitor])
        return Image.frombytes('RGB', shot.size, shot.rgb)

    def close(self):
        if self.screen is not None:
            self.screen.close()
            self.screen = None


class DesktopTrack(VideoStreamTrack):
    def __init__(self, capture, fps=15, width=1280, on_error=None):
        super().__init__()
        self.capture, self.fps, self.width, self.on_error = capture, fps, width, on_error
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix='omnipad-screen')
        self.started = None
        self.index = 0
        self.closed = False
        self.failed = False

    async def probe(self):
        image = await asyncio.get_running_loop().run_in_executor(self.executor, self.capture.frame)
        if image.width <= 0 or image.height <= 0:
            raise ValueError('empty_screen')

    def _frame(self):
        image = self.capture.frame()
        from PIL import Image
        image.thumbnail((self.width, 720), Image.Resampling.BILINEAR)
        return VideoFrame.from_image(image)

    async def recv(self):
        if self.readyState != 'live':
            raise MediaStreamError
        if self.started is None:
            self.started = time.monotonic()
        # Schedule relative to the current frame; never accumulate stale frames.
        due = self.started + self.index / self.fps
        await asyncio.sleep(max(0, due - time.monotonic()))
        try:
            frame = await asyncio.get_running_loop().run_in_executor(self.executor, self._frame)
        except Exception:
            if not self.failed and self.on_error:
                self.failed = True
                asyncio.create_task(self.on_error())
            raise MediaStreamError
        if self.readyState != 'live':
            raise MediaStreamError
        frame.pts = int((time.monotonic() - self.started) * 90000)
        frame.time_base = fractions.Fraction(1, 90000)
        self.index = max(self.index + 1, int((time.monotonic() - self.started) * self.fps))
        return frame

    async def aclose(self):
        if self.closed:
            return
        self.closed = True
        self.stop()
        try:
            await asyncio.get_running_loop().run_in_executor(self.executor, self.capture.close)
        except Exception:
            pass
        finally:
            self.executor.shutdown(wait=False, cancel_futures=True)


class ScreenSession:
    def __init__(self, emit, capture_factory=None, fps=15, width=1280):
        self.emit = emit
        self.capture_factory = capture_factory or DesktopCapture
        self.fps, self.width = fps, width
        self.pc = self.track = self.task = None
        self.generation = 0
        self.lock = asyncio.Lock()

    async def start(self, sdp, request_id, monitor=None):
        if monitor is not None and (type(monitor) is not int or not 1 <= monitor <= 256):
            raise ValueError("invalid_monitor")
        if not isinstance(sdp, str) or not 1 <= len(sdp) <= 48000 or 'm=video' not in sdp:
            raise ValueError('invalid_screen_offer')
        if type(request_id) is not int or not 1 <= request_id <= 2**31-1:
            raise ValueError('invalid_screen_id')
        if self.pc is not None or (self.task is not None and not self.task.done()):
            await self.emit({'type':'mirror_error','id':request_id,'reason':'busy'})
            return
        self.generation += 1
        generation = self.generation
        self.task = asyncio.create_task(self._negotiate(sdp, request_id, generation, monitor))

    async def _negotiate(self, sdp, request_id, generation, monitor):
        async def capture_error():
            if generation == self.generation:
                try:
                    await self.emit({'type':'mirror_error','id':request_id,'reason':'capture_unavailable'})
                finally:
                    await self.stop()
        try:
            capture = self.capture_factory()
            if monitor is not None:
                capture.monitor = monitor
            self.track = DesktopTrack(capture, self.fps, self.width, capture_error)
            await self.track.probe()
            self.pc = RTCPeerConnection(RTCConfiguration(iceServers=[]))
            pc = self.pc
            @pc.on('connectionstatechange')
            async def connectionstatechange():
                if pc.connectionState == 'failed' and generation == self.generation:
                    try:
                        await self.emit({'type':'mirror_error','id':request_id,'reason':'connection_failed'})
                    finally:
                        await self.stop()
            await pc.setRemoteDescription(RTCSessionDescription(sdp=sdp, type='offer'))
            pc.addTrack(self.track)
            await pc.setLocalDescription(await pc.createAnswer())
            if generation == self.generation:
                await self.emit({'type':'mirror_answer','id':request_id,'sdp':pc.localDescription.sdp,'sdp_type':'answer','fps':self.fps,'max_width':self.width})
        except asyncio.CancelledError:
            raise
        except Exception:
            if generation == self.generation:
                try:
                    await self.emit({'type':'mirror_error','id':request_id,'reason':'capture_or_negotiation_failed'})
                finally:
                    await self.stop()

    async def stop(self):
        async with self.lock:
            self.generation += 1
            task, self.task = self.task, None
            if task is not None and task is not asyncio.current_task() and not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
            pc, track = self.pc, self.track
            self.pc = self.track = None
            try:
                if pc is not None:
                    await pc.close()
            finally:
                if track is not None:
                    await track.aclose()
