package es.lexia.piloto;

import android.Manifest;
import android.app.*;
import android.content.*;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.net.Uri;
import android.os.*;
import android.text.*;
import android.text.style.*;
import android.view.*;
import android.widget.*;
import ai.moonshine.voice.*;
import org.json.*;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;
import java.util.regex.Matcher;

/** Piloto experimental: ASR nativo local; solo descarga modelos, no sube audio. */
public class MainActivity extends Activity {
    private final ExecutorService worker=Executors.newSingleThreadExecutor();
    private final Handler main=new Handler(Looper.getMainLooper());
    private MicTranscriber mic;
    private Spinner storyChoice,modelChoice,guideChoice,intervalChoice,marginChoice,advanceChoice;
    private double selectedNativeInterval=.125;
    private TextView storyView,status,hypothesis,metrics;
    private ScrollView reading;
    private Button prepare,start,stop,export;
    private String[] storyFiles;
    private String story="",history="",lastHypothesis="";
    private final List<int[]> ranges=new ArrayList<>();
    private ReadingTracker tracker;
    private boolean prepared=false,listening=false,starting=false,finishing=false;
    private volatile boolean dead=false,resumed=false;
    private int selectedArch=JNI.MOONSHINE_MODEL_ARCH_TINY_STREAMING,group=2;
    private long started=0,cpuStart=0;
    private JSONObject record,modelInfo=new JSONObject();
    private JSONArray updates;
    private File lastReport;

    @Override public void onCreate(Bundle state){
        super.onCreate(state);getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(18,20,18,16);root.setFitsSystemWindows(true);root.setBackgroundColor(Color.rgb(244,247,243));
        TextView title=new TextView(this);title.setText("lexia · piloto Android");title.setTextSize(25);root.addView(title);
        TextView subtitle=new TextView(this);subtitle.setText("Reconocimiento dentro del móvil · español\nPreparación inicial con Wi-Fi; después prueba sin conexión.");root.addView(subtitle);
        storyChoice=spinner(root,new String[]{"Cargando textos…"});
        modelChoice=spinner(root,new String[]{"Moonshine Tiny español · SDK nativo","Moonshine Small español · SDK nativo"});
        guideChoice=spinner(root,new String[]{"Dos palabras móviles","Tres palabras móviles","Una palabra"});
        intervalChoice=spinner(root,new String[]{"ASR 0,25 s","ASR 0,125 s"});intervalChoice.setSelection(1);
        marginChoice=spinner(root,new String[]{"Contexto local original","Buscar desde 5 palabras atrás · experimental"});
        advanceChoice=spinner(root,new String[]{"Seguidor original · referencia","Avance con apoyo · experimental"});
        LinearLayout buttons=new LinearLayout(this);root.addView(buttons);
        prepare=button(buttons,"Preparar");start=button(buttons,"Empezar");stop=button(buttons,"Terminar");
        status=new TextView(this);status.setText("Selecciona texto y pulsa Preparar.");root.addView(status);
        reading=new ScrollView(this);storyView=new TextView(this);storyView.setTextSize(25);storyView.setLineSpacing(12,1.1f);storyView.setPadding(12,18,12,18);reading.addView(storyView);root.addView(reading,new LinearLayout.LayoutParams(-1,0,1));
        metrics=new TextView(this);metrics.setTextSize(12);root.addView(metrics);
        hypothesis=new TextView(this);hypothesis.setTextSize(12);hypothesis.setMaxLines(3);root.addView(hypothesis);
        export=new Button(this);export.setText("Exportar registro JSON");root.addView(export);setContentView(root);
        start.setEnabled(false);stop.setEnabled(false);export.setEnabled(false);
        File[] saved=getFilesDir().listFiles((dir,name)->name.startsWith("lexia_")&&name.endsWith(".json"));
        if(saved!=null&&saved.length>0){Arrays.sort(saved,Comparator.comparingLong(File::lastModified));lastReport=saved[saved.length-1];export.setEnabled(true);}
        try{storyFiles=getAssets().list("textos");Arrays.sort(storyFiles);storyChoice.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,storyFiles));}catch(Exception e){showError(e);}
        storyChoice.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){loadStory();}});
        guideChoice.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){group=new int[]{2,3,1}[pos];if(tracker!=null)paint(tracker.position);}});
        modelChoice.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){prepared=false;start.setEnabled(false);}});
        intervalChoice.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener(){public void onNothingSelected(AdapterView<?> p){}public void onItemSelected(AdapterView<?> p,View v,int pos,long id){prepared=false;start.setEnabled(false);}});
        prepare.setOnClickListener(v->prepareModel());start.setOnClickListener(v->requestStart());stop.setOnClickListener(v->stopReading("boton"));
        export.setOnClickListener(v->{if(lastReport!=null){Intent i=new Intent(Intent.ACTION_CREATE_DOCUMENT);i.setType("application/json");i.addCategory(Intent.CATEGORY_OPENABLE);i.putExtra(Intent.EXTRA_TITLE,lastReport.getName());startActivityForResult(i,42);}});
    }
    private Spinner spinner(LinearLayout root,String[] items){Spinner s=new Spinner(this);s.setAdapter(new ArrayAdapter<>(this,android.R.layout.simple_spinner_dropdown_item,items));root.addView(s);return s;}
    private Button button(LinearLayout root,String text){Button b=new Button(this);b.setText(text);root.addView(b,new LinearLayout.LayoutParams(0,-2,1));return b;}
    private void lock(boolean busy){prepare.setEnabled(!busy);storyChoice.setEnabled(!busy);modelChoice.setEnabled(!busy);guideChoice.setEnabled(!busy);intervalChoice.setEnabled(!busy);marginChoice.setEnabled(!busy);advanceChoice.setEnabled(!busy);start.setEnabled(!busy&&prepared);stop.setEnabled(listening&&!finishing);}
    private void loadStory(){try{story=NormalizerText(readAsset("textos/"+storyFiles[storyChoice.getSelectedItemPosition()]));tracker=new ReadingTracker(story,marginChoice.getSelectedItemPosition()==1?5:12,advanceChoice.getSelectedItemPosition()==1);ranges.clear();Matcher m=ReadingTracker.TOKEN.matcher(story);while(m.find())ranges.add(new int[]{m.start(),m.end()});paint(0);}catch(Exception e){showError(e);}}
    private String NormalizerText(String s){return java.text.Normalizer.normalize(s,java.text.Normalizer.Form.NFC);}
    private String readAsset(String path)throws IOException{try(InputStream in=getAssets().open(path);ByteArrayOutputStream out=new ByteArrayOutputStream()){byte[] buffer=new byte[4096];int n;while((n=in.read(buffer))>0)out.write(buffer,0,n);return out.toString("UTF-8");}}
    private void paint(int confirmed){
        SpannableString text=new SpannableString(story);int[] guide=ReadingGuide.range(confirmed,ranges.size(),group);
        int first=guide[0]<guide[1]?guide[0]:-1;
        if(first>=0){text.setSpan(new BackgroundColorSpan(Color.rgb(255,215,133)),ranges.get(first)[0],ranges.get(guide[1]-1)[1],Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);}
        if(confirmed>0&&confirmed<=ranges.size()){int[] r=ranges.get(confirmed-1);text.setSpan(new UnderlineSpan(),r[0],r[1],Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);}
        storyView.setText(text);
        if(first>=0&&storyView.getLayout()!=null){int top=storyView.getLayout().getLineTop(storyView.getLayout().getLineForOffset(ranges.get(first)[0]));if(top<reading.getScrollY()||top>reading.getScrollY()+reading.getHeight()-80)reading.smoothScrollTo(0,Math.max(0,top-reading.getHeight()/3));}
    }
    private void prepareModel(){
        if(listening||starting)return;prepared=false;lock(true);status.setText("Preparando modelo español en este móvil…");
        selectedArch=modelChoice.getSelectedItemPosition()==0?JNI.MOONSHINE_MODEL_ARCH_TINY_STREAMING:JNI.MOONSHINE_MODEL_ARCH_SMALL_STREAMING;
        final int arch=selectedArch;
        selectedNativeInterval=new double[]{.25,.125}[intervalChoice.getSelectedItemPosition()];
        final double nativeInterval=selectedNativeInterval;
        worker.execute(()->{try{
            if(mic!=null){mic.close();mic=null;}
            MicTranscriber next=new MicTranscriber(this).language("es").modelArch(arch)
                .onText(text->consume(text,false,null))
                .onLine(line->consume(line.text==null?"":line.text,true,line))
                .onError(error->runOnUiThread(()->{showError(error);stopReading("error_asr");}))
                .onProgress((fraction,file)->runOnUiThread(()->{if(!dead)status.setText("Descarga/preparación: "+(int)(fraction*100)+" % · "+file);}));
            next.options(new TranscriberOption("transcription_interval",String.valueOf(nativeInterval)));
            next.setUpdateInterval(.125);next.load();mic=next;
            JSONObject identity=new JSONObject();identity.put("sdk","ai.moonshine:moonshine-voice:0.1.5");identity.put("architecture",arch);identity.put("language","es");
            identity.put("native_options",new JSONObject().put("transcription_interval",String.valueOf(nativeInterval)));
            identity.put("dependencies",new JSONObject(Transcriber.getSttDependencies("es",Arrays.asList(new TranscriberOption("model_arch",String.valueOf(arch))))));
            File modelDir=ModelCache.directoryFor(this,ModelSpec.stt("es",arch,false),null);JSONArray files=new JSONArray();hashFiles(modelDir,modelDir,files);identity.put("files",files);modelInfo=identity;
            runOnUiThread(()->{if(dead)return;prepared=true;lock(false);status.setText("Preparado · modelo dentro del móvil. Puedes activar modo avión y empezar.");});
        }catch(Throwable e){runOnUiThread(()->{prepared=false;lock(false);showError(e);});}});
    }
    private void requestStart(){
        if(!prepared||listening||starting)return;
        if(checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED){requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},7);return;}
        begin();
    }
    @Override public void onRequestPermissionsResult(int req,String[] permissions,int[] grants){super.onRequestPermissionsResult(req,permissions,grants);if(req==7&&grants.length>0&&grants[0]==PackageManager.PERMISSION_GRANTED)begin();}
    private void begin(){
        if(!prepared||listening||starting)return;starting=true;lock(true);loadStory();history="";lastHypothesis="";
        started=SystemClock.elapsedRealtime();cpuStart=android.os.Process.getElapsedCpuTime();updates=new JSONArray();
        try{record=new JSONObject();record.put("created_at_utc",java.time.Instant.now().toString());record.put("story",storyFiles[storyChoice.getSelectedItemPosition()]);record.put("story_sha256",hash(story.getBytes(StandardCharsets.UTF_8)));record.put("guide_words",group);record.put("guide_policy","sliding_next_words");record.put("app_version","0.5-piloto");record.put("tracker_advance_policy",advanceChoice.getSelectedItemPosition()==1?"terminal_and_recent":"original");record.put("tracker_rule","textual_configurable_local_margin");record.put("tracker_before_words",marginChoice.getSelectedItemPosition()==1?5:12);record.put("tracker_local_search_offset_words",marginChoice.getSelectedItemPosition()==1?6:12);record.put("tracker_after_words",24);record.put("tracker_global_recovery_enabled",true);record.put("native_transcription_interval_requested_seconds",selectedNativeInterval);record.put("runtime",modelInfo);record.put("update_interval_requested_seconds",.125);record.put("pipeline","Moonshine SDK nativo streaming; VAD/segmentación interna. Configuración distinta de las ventanas PyTorch del PC.");record.put("device",deviceInfo());record.put("battery_start",battery());record.put("updates",updates);record.put("audio_saved",false);record.put("notice","Sin referencia humana temporal: no calcula error de posición ni latencia acústica real. PSS muestreado de toda la app; latencia del SDK por línea cuando está disponible.");}catch(Exception e){showError(e);starting=false;lock(false);return;}
        lastReport=new File(getFilesDir(),"lexia_"+System.currentTimeMillis()+".json");export.setEnabled(false);
        worker.execute(()->{try{if(!resumed)throw new IllegalStateException("La app debe estar visible");mic.start();runOnUiThread(()->{starting=false;if(dead)return;listening=true;lock(true);stop.setEnabled(true);status.setText("Lee a tu ritmo · audio procesado dentro del móvil");main.post(sample);});}catch(Throwable e){runOnUiThread(()->{starting=false;lock(false);showError(e);});}});
    }
    private void consume(String current,boolean completed,TranscriptLine line){
        if(dead||(!listening&&!finishing))return;
        String combined=history+" "+current;
        int before=tracker.position;long trackerStart=System.nanoTime();tracker.update(combined,current);long trackerNanos=System.nanoTime()-trackerStart;paint(tracker.position);hypothesis.setText(current);
        try{JSONObject r=new JSONObject();r.put("callback_elapsed_ms",SystemClock.elapsedRealtime()-started);r.put("position",tracker.position);r.put("movement",tracker.position-before);r.put("tracker_compute_ms",trackerNanos/1000000.0);r.put("hypothesis",combined);r.put("asr_current_line",current);r.put("tracker_mode",tracker.lastMode);r.put("tracker_reason",tracker.lastReason);r.put("tracker_search",tracker.lastSearch);r.put("tracker_exact_matches",tracker.lastMatches);r.put("tracker_hypothesis_words",tracker.lastHypothesisWords);r.put("tracker_edit_cost",tracker.lastEditCost);r.put("tracker_candidate",tracker.lastCandidate==null?JSONObject.NULL:tracker.lastCandidate);r.put("line_complete",completed);if(line!=null){r.put("sdk_last_transcription_latency_ms",line.lastTranscriptionLatencyMs);r.put("sdk_line_start_seconds",line.startTime);r.put("sdk_line_duration_seconds",line.duration);}updates.put(r);}catch(Exception e){showError(e);}
        lastHypothesis=combined;
        if(completed){history=(history+" "+current).trim();List<String> tail=ReadingTracker.tokens(history);if(tail.size()>100)history=String.join(" ",tail.subList(tail.size()-100,tail.size()));}
    }
    private final Runnable sample=new Runnable(){public void run(){if(!listening&&!finishing)return;try{JSONObject s=new JSONObject();s.put("elapsed_ms",SystemClock.elapsedRealtime()-started);s.put("pss_kib",Debug.getPss());s.put("cpu_ms_app",android.os.Process.getElapsedCpuTime()-cpuStart);JSONArray samples=record.optJSONArray("resource_samples");if(samples==null){samples=new JSONArray();record.put("resource_samples",samples);}samples.put(s);metrics.setText("Posición "+tracker.position+"/"+tracker.story.size()+" · RAM PSS "+(s.getLong("pss_kib")/1024)+" MiB · "+(s.getLong("elapsed_ms")/1000)+" s");persistSnapshot();}catch(Exception e){showError(e);}if(listening)main.postDelayed(this,1000);}};
    private void stopReading(String reason){
        if((!listening&&!starting)||finishing)return;finishing=true;listening=false;stop.setEnabled(false);status.setText("Cerrando micrófono y guardando…");
        worker.execute(()->{try{if(mic!=null){mic.stop();mic.close();mic=null;}}catch(Throwable ignored){}
            runOnUiThread(()->{try{if(record!=null){record.put("finished",true);record.put("stop_reason",reason);record.put("final_position",tracker.position);record.put("wall_ms",SystemClock.elapsedRealtime()-started);record.put("cpu_ms_app",android.os.Process.getElapsedCpuTime()-cpuStart);record.put("battery_end",battery());persistSnapshot();}}catch(Exception e){showError(e);}finishing=false;starting=false;prepared=false;main.removeCallbacks(sample);lock(false);export.setEnabled(lastReport!=null);status.setText("Terminada · registro local guardado. Preparar para otra toma.");});});
    }
    private void persistSnapshot()throws Exception{
        if(record==null||lastReport==null)return;final String json=record.toString(2);final File file=lastReport;
        worker.execute(()->{android.util.AtomicFile atomic=new android.util.AtomicFile(file);FileOutputStream out=null;try{out=atomic.startWrite();out.write(json.getBytes(StandardCharsets.UTF_8));atomic.finishWrite(out);}catch(Exception e){if(out!=null)atomic.failWrite(out);runOnUiThread(()->showError(e));}});
    }
    private JSONObject deviceInfo()throws Exception{JSONObject j=new JSONObject();j.put("manufacturer",Build.MANUFACTURER);j.put("model",Build.MODEL);j.put("android",Build.VERSION.RELEASE);j.put("sdk_int",Build.VERSION.SDK_INT);j.put("abis",new JSONArray(Arrays.asList(Build.SUPPORTED_ABIS)));ActivityManager.MemoryInfo mem=new ActivityManager.MemoryInfo();((ActivityManager)getSystemService(ACTIVITY_SERVICE)).getMemoryInfo(mem);j.put("total_ram_bytes",mem.totalMem);j.put("available_ram_bytes_start",mem.availMem);return j;}
    private JSONObject battery()throws Exception{JSONObject j=new JSONObject();Intent b=registerReceiver(null,new IntentFilter(Intent.ACTION_BATTERY_CHANGED));if(b!=null){j.put("level",b.getIntExtra(BatteryManager.EXTRA_LEVEL,-1));j.put("scale",b.getIntExtra(BatteryManager.EXTRA_SCALE,-1));j.put("temperature_c_battery",b.getIntExtra(BatteryManager.EXTRA_TEMPERATURE,0)/10.0);j.put("plugged",b.getIntExtra(BatteryManager.EXTRA_PLUGGED,0));}return j;}
    private void hashFiles(File base,File folder,JSONArray out)throws Exception{File[] files=folder.listFiles();if(files==null)return;Arrays.sort(files);for(File f:files){if(f.isDirectory())hashFiles(base,f,out);else{MessageDigest digest=MessageDigest.getInstance("SHA-256");try(InputStream in=new FileInputStream(f)){byte[] buffer=new byte[1024*1024];int n;while((n=in.read(buffer))>0)digest.update(buffer,0,n);}JSONObject item=new JSONObject();item.put("file",base.toPath().relativize(f.toPath()).toString());item.put("bytes",f.length());item.put("sha256",hex(digest.digest()));out.put(item);}}}
    private String hash(byte[] data)throws Exception{return hex(MessageDigest.getInstance("SHA-256").digest(data));}
    private String hex(byte[] data){StringBuilder b=new StringBuilder();for(byte value:data)b.append(String.format(Locale.ROOT,"%02x",value&255));return b.toString();}
    private void showError(Throwable e){if(dead)return;status.setText("Incidencia: "+e.getMessage());}
    @Override protected void onStart(){super.onStart();resumed=true;}
    @Override protected void onStop(){resumed=false;if(listening||starting)stopReading("app_en_segundo_plano");super.onStop();}
    @Override protected void onDestroy(){dead=true;main.removeCallbacks(sample);worker.execute(()->{if(mic!=null)mic.close();});worker.shutdown();super.onDestroy();}
    @Override protected void onActivityResult(int request,int result,Intent data){super.onActivityResult(request,result,data);if(request==42&&result==RESULT_OK&&data!=null&&lastReport!=null){final Uri uri=data.getData();final File file=lastReport;worker.execute(()->{try(InputStream in=new FileInputStream(file);OutputStream out=getContentResolver().openOutputStream(uri)){if(out==null)throw new IOException("No se pudo abrir el destino");byte[] buf=new byte[8192];int n;while((n=in.read(buf))>0)out.write(buf,0,n);runOnUiThread(()->status.setText("Registro exportado"));}catch(Exception e){runOnUiThread(()->showError(e));}});}}
}
