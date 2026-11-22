package id.omnipad.tv;

import fi.iki.elonen.NanoHTTPD;
import org.json.JSONObject;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;
import java.util.HashSet;
import java.util.Arrays;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class RemoteServer extends NanoHTTPD {
    private final RemoteAccessibilityService service;
    private volatile String secret;
    private final String page;
    private long window=0;private int count=0;
    private static final Set<String> ACTIONS=new HashSet<>(Arrays.asList("up","down","left","right","ok","back","home","volume_up","volume_down","mute","play_pause","previous","next"));
    public RemoteServer(RemoteAccessibilityService service) throws Exception{
        super(8765);this.service=service;rotate();
        try(java.io.InputStream input=service.getAssets().open("remote.html")){page=new String(input.readAllBytes(),StandardCharsets.UTF_8);}
        setAsyncRunner(new BoundedRunner());
    }
    public String token(){return secret;}
    public void rotate(){byte[] bytes=new byte[24];new SecureRandom().nextBytes(bytes);secret=Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);}
    private synchronized boolean limit(){long now=System.nanoTime();if(now-window>1_000_000_000L){window=now;count=0;}return ++count<=20;}
    private Response reply(Response.Status status,String body){Response r=newFixedLengthResponse(status,"application/json; charset=utf-8",body);r.addHeader("Cache-Control","no-store");r.addHeader("X-Content-Type-Options","nosniff");return r;}
    @Override public Response serve(IHTTPSession session){
        if(session.getMethod()==Method.GET&&session.getUri().equals("/")){
            Response r=newFixedLengthResponse(Response.Status.OK,"text/html; charset=utf-8",page);
            r.addHeader("Cache-Control","no-store");r.addHeader("Referrer-Policy","no-referrer");r.addHeader("X-Frame-Options","DENY");r.addHeader("Content-Security-Policy","default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'");return r;
        }
        if(session.getMethod()!=Method.POST||!session.getUri().equals("/command"))return reply(Response.Status.NOT_FOUND,"{\"error\":\"not_found\"}");
        String host=session.getHeaders().get("host"),origin=session.getHeaders().get("origin");
        if(host==null||!host.matches("[0-9.]+:8765")||!("http://"+host).equals(origin))return reply(Response.Status.FORBIDDEN,"{\"error\":\"origin\"}");
        String auth=session.getHeaders().get("authorization");
        if(auth==null||!MessageDigest.isEqual(auth.getBytes(StandardCharsets.UTF_8),("Bearer "+secret).getBytes(StandardCharsets.UTF_8)))return reply(Response.Status.UNAUTHORIZED,"{\"error\":\"pairing\"}");
        if(!limit())return reply(Response.Status.BAD_REQUEST,"{\"error\":\"too_fast\"}");
        try{
            String length=session.getHeaders().get("content-length");
            if(session.getHeaders().containsKey("transfer-encoding")||length==null||Integer.parseInt(length)>1024||Integer.parseInt(length)<2)return reply(Response.Status.BAD_REQUEST,"{\"error\":\"size\"}");
            if(!session.getHeaders().getOrDefault("content-type","").startsWith("application/json"))return reply(Response.Status.BAD_REQUEST,"{\"error\":\"format\"}");
            Map<String,String> body=new HashMap<>();session.parseBody(body);
            String raw=body.getOrDefault("postData","");if(raw.length()>1024)return reply(Response.Status.BAD_REQUEST,"{\"error\":\"size\"}");
            JSONObject json=new JSONObject(raw);String action=json.optString("action","");
            if(action.equals("ping"))return reply(Response.Status.OK,"{\"ok\":true}");
            if(!ACTIONS.contains(action))return reply(Response.Status.BAD_REQUEST,"{\"error\":\"action\"}");
            boolean accepted=service.command(action);
            return reply(Response.Status.OK,accepted?"{\"ok\":true}":"{\"error\":\"unsupported\"}");
        }catch(Exception e){return reply(Response.Status.BAD_REQUEST,"{\"error\":\"request\"}");}
    }
    private static final class BoundedRunner implements AsyncRunner {
        private final ThreadPoolExecutor executor=new ThreadPoolExecutor(2,2,0,TimeUnit.MILLISECONDS,new ArrayBlockingQueue<>(8));
        private final Set<ClientHandler> clients=java.util.Collections.synchronizedSet(new HashSet<>());
        public void exec(ClientHandler handler){clients.add(handler);try{executor.execute(handler);}catch(java.util.concurrent.RejectedExecutionException e){clients.remove(handler);handler.close();}}
        public void closed(ClientHandler handler){clients.remove(handler);}
        public void closeAll(){ClientHandler[] snapshot;synchronized(clients){snapshot=clients.toArray(new ClientHandler[0]);clients.clear();}for(ClientHandler client:snapshot)client.close();executor.shutdownNow();}
    }
}
