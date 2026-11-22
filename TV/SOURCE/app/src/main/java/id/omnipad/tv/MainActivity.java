package id.omnipad.tv;

import android.app.Activity;
import android.app.AlertDialog;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.Settings;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.net.ConnectivityManager;
import android.net.LinkProperties;
import android.net.LinkAddress;
import android.widget.*;
import android.view.View;
import com.google.zxing.BarcodeFormat;
import com.google.zxing.qrcode.QRCodeWriter;
import com.google.zxing.common.BitMatrix;
import java.net.Inet4Address;

public class MainActivity extends Activity {
    private TextView status,urlText;
    private ImageView qr;
    private final Handler handler=new Handler(Looper.getMainLooper());
    private String lastUrl="";
    private final Runnable refresh=new Runnable(){ public void run(){update();handler.postDelayed(this,2000);} };
    @Override public void onCreate(Bundle bundle){
        super.onCreate(bundle);
        ScrollView scroll=new ScrollView(this);scroll.setBackgroundColor(Color.rgb(247,246,243));
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.HORIZONTAL);root.setPadding(48,36,48,36);scroll.addView(root);
        LinearLayout left=new LinearLayout(this);left.setOrientation(LinearLayout.VERTICAL);root.addView(left,new LinearLayout.LayoutParams(0,-2,1));
        TextView title=new TextView(this);title.setText("OmniPad Receiver");title.setTextSize(32);title.setTextColor(Color.rgb(37,41,35));left.addView(title);
        status=new TextView(this);status.setTextSize(19);status.setTextColor(Color.rgb(60,68,54));status.setPadding(0,18,24,24);left.addView(status);
        button(left,"1. Aktifkan kontrol",()->new AlertDialog.Builder(this).setTitle("Izinkan HP mengontrol TV?").setMessage("OmniPad memakai layanan aksesibilitas untuk menjalankan tombol arah, OK, Kembali dan Home atas perintah HP. Siapa pun yang memiliki tautan pairing dapat mengirim kontrol pada Wi-Fi yang sama. Aplikasi tidak membaca isi layar atau merekam layar. Nonaktifkan layanan untuk menghentikan akses.").setPositiveButton("Buka pengaturan",(d,w)->{try{startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS));}catch(Exception e){startActivity(new Intent(Settings.ACTION_SETTINGS));}}).setNegativeButton("Nanti",null).show());
        button(left,"Ganti tautan pairing",()->{RemoteAccessibilityService s=RemoteAccessibilityService.instance;if(s!=null){s.rotate();lastUrl="";update();}});
        button(left,"Hentikan receiver",()->{RemoteAccessibilityService s=RemoteAccessibilityService.instance;if(s!=null)s.disableSelf();});
        TextView help=new TextView(this);help.setText("Setelah diaktifkan, pilih OmniPad Remote pada pengaturan aksesibilitas. Kembali ke sini, pindai QR dengan HP, lalu tekan Hubungkan. Gunakan Wi-Fi pribadi yang sama.\n\nReceiver dasar ini belum mendukung mouse, keyboard teks, atau stik game. Efek media mengikuti aplikasi TV yang aktif.");help.setTextSize(15);help.setTextColor(Color.rgb(67,78,56));help.setPadding(0,24,24,0);left.addView(help);
        LinearLayout right=new LinearLayout(this);right.setOrientation(LinearLayout.VERTICAL);right.setPadding(32,12,0,0);root.addView(right,new LinearLayout.LayoutParams(300,-2));
        qr=new ImageView(this);right.addView(qr,new LinearLayout.LayoutParams(268,268));
        urlText=new TextView(this);urlText.setTextSize(14);urlText.setTextColor(Color.rgb(37,41,35));urlText.setPadding(0,14,0,0);urlText.setTextIsSelectable(true);right.addView(urlText);
        setContentView(scroll);
    }
    private void button(LinearLayout parent,String title,Runnable action){Button b=new Button(this);b.setText(title);b.setTextSize(17);b.setMinHeight(56);b.setOnClickListener(v->action.run());parent.addView(b,new LinearLayout.LayoutParams(-1,-2));}
    private String ip(){
        try{ConnectivityManager cm=(ConnectivityManager)getSystemService(CONNECTIVITY_SERVICE);LinkProperties link=cm.getLinkProperties(cm.getActiveNetwork());if(link!=null)for(LinkAddress address:link.getLinkAddresses())if(address.getAddress() instanceof Inet4Address&&!address.getAddress().isLoopbackAddress())return address.getAddress().getHostAddress();}catch(Exception ignored){}
        return "";
    }
    private void update(){
        RemoteAccessibilityService s=RemoteAccessibilityService.instance;
        if(s==null){status.setText("Belum aktif. Aktifkan OmniPad Remote pada pengaturan aksesibilitas TV.");qr.setImageDrawable(null);urlText.setText("");lastUrl="";return;}
        if(!s.error.isEmpty()){status.setText(s.error);qr.setImageDrawable(null);urlText.setText("");return;}
        String ip=ip();if(ip.isEmpty()){status.setText("Hubungkan TV ke Wi-Fi atau kabel LAN lebih dahulu.");qr.setImageDrawable(null);urlText.setText("");return;}
        String url="http://"+ip+":8765/#"+s.token();status.setText("Receiver aktif. Pindai QR dengan HP, lalu tekan Hubungkan. Anda dapat membuka aplikasi TV lain setelah terhubung.");
        if(url.equals(lastUrl))return;
        try{BitMatrix matrix=new QRCodeWriter().encode(url,BarcodeFormat.QR_CODE,384,384);Bitmap bitmap=Bitmap.createBitmap(384,384,Bitmap.Config.RGB_565);for(int y=0;y<384;y++)for(int x=0;x<384;x++)bitmap.setPixel(x,y,matrix.get(x,y)?Color.BLACK:Color.WHITE);qr.setImageBitmap(bitmap);urlText.setText(url);lastUrl=url;}catch(Exception e){urlText.setText(url);}
    }
    @Override protected void onResume(){super.onResume();handler.post(refresh);}
    @Override protected void onPause(){handler.removeCallbacks(refresh);super.onPause();}
}
