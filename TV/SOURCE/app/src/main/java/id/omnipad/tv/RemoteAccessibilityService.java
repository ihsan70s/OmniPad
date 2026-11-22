package id.omnipad.tv;

import android.accessibilityservice.AccessibilityService;
import android.content.Intent;
import android.media.AudioManager;
import android.os.Handler;
import android.os.Looper;
import android.view.KeyEvent;
import android.view.accessibility.AccessibilityEvent;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicBoolean;

public class RemoteAccessibilityService extends AccessibilityService {
    public static volatile RemoteAccessibilityService instance;
    private RemoteServer server;
    public volatile String error = "";
    private final Handler main = new Handler(Looper.getMainLooper());
    @Override protected void onServiceConnected() {
        instance=this;
        try { server=new RemoteServer(this); server.start(2000,false); }
        catch(Exception e){ error="Receiver belum berjalan. Nonaktifkan lalu aktifkan layanan."; }
    }
    public String token(){ return server==null?"":server.token(); }
    public void rotate(){ if(server!=null)server.rotate(); }
    public boolean command(String action) throws InterruptedException {
        CountDownLatch done=new CountDownLatch(1);
        AtomicBoolean pending=new AtomicBoolean(true),result=new AtomicBoolean(false);
        main.post(()->{if(pending.compareAndSet(true,false))try{result.set(execute(action));}catch(Exception ignored){}finally{done.countDown();}});
        if(!done.await(1200,TimeUnit.MILLISECONDS)){ pending.set(false);return false; }
        return result.get();
    }
    private boolean execute(String action){
        int global;
        switch(action){
            case "up":global=GLOBAL_ACTION_DPAD_UP;break;
            case "down":global=GLOBAL_ACTION_DPAD_DOWN;break;
            case "left":global=GLOBAL_ACTION_DPAD_LEFT;break;
            case "right":global=GLOBAL_ACTION_DPAD_RIGHT;break;
            case "ok":global=GLOBAL_ACTION_DPAD_CENTER;break;
            case "back":global=GLOBAL_ACTION_BACK;break;
            case "home":global=GLOBAL_ACTION_HOME;break;
            default:global=0;
        }
        if(global!=0)return performGlobalAction(global);
        AudioManager audio=(AudioManager)getSystemService(AUDIO_SERVICE);
        if(audio==null)return false;
        switch(action){
            case "volume_up":audio.adjustStreamVolume(AudioManager.STREAM_MUSIC,AudioManager.ADJUST_RAISE,AudioManager.FLAG_SHOW_UI);return true;
            case "volume_down":audio.adjustStreamVolume(AudioManager.STREAM_MUSIC,AudioManager.ADJUST_LOWER,AudioManager.FLAG_SHOW_UI);return true;
            case "mute":audio.adjustStreamVolume(AudioManager.STREAM_MUSIC,AudioManager.ADJUST_TOGGLE_MUTE,AudioManager.FLAG_SHOW_UI);return true;
            default:
                int code;
                if(action.equals("play_pause"))code=KeyEvent.KEYCODE_MEDIA_PLAY_PAUSE;
                else if(action.equals("next"))code=KeyEvent.KEYCODE_MEDIA_NEXT;
                else if(action.equals("previous"))code=KeyEvent.KEYCODE_MEDIA_PREVIOUS;
                else return false;
                audio.dispatchMediaKeyEvent(new KeyEvent(KeyEvent.ACTION_DOWN,code));
                audio.dispatchMediaKeyEvent(new KeyEvent(KeyEvent.ACTION_UP,code));return true;
        }
    }
    @Override public void onAccessibilityEvent(AccessibilityEvent event) { /* no UI content collected */ }
    @Override public void onInterrupt() { }
    @Override public boolean onUnbind(Intent intent){ shutdown();return super.onUnbind(intent); }
    @Override public void onDestroy(){ shutdown();super.onDestroy(); }
    private void shutdown(){ if(server!=null){server.stop();server=null;}if(instance==this)instance=null; }
}
