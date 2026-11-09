'use strict';
const $=id=>document.getElementById(id);
let cfg,session=null,stream,context,source,node,gain,ring,cursor=0,total=0,lastSent=0,busy=false,active=false,stopping=false,flushResolve,firstPerf=null,inflight=Promise.resolve(),saved=[],wavURL;
let pendingRender=null;
async function request(path,data,raw=false,extraHeaders={}){
  const options=data===undefined?{}:{method:'POST',headers:{'X-Lexia-Token':cfg.token,'Content-Type':raw?'application/octet-stream':'application/json',...extraHeaders},body:raw?data:JSON.stringify(data)};
  const response=await fetch(path,options);const value=await response.json();if(!response.ok)throw new Error(value.error||'No se pudo completar la petición');return value;
}
function note(text){$('status').textContent=text;}
function draw(){
  const story=cfg.stories.find(s=>s.id===$('story').value);$('title').textContent=story.id.replace('.txt','');$('text').replaceChildren();
  // Misma separación Unicode por letras/números que el tokenizador Python.
  const words=/[\p{L}\p{N}]+(?:['’][\p{L}\p{N}]+)*/gu;let end=0,index=0;
  for(const match of story.text.matchAll(words)){
    $('text').append(document.createTextNode(story.text.slice(end,match.index)));
    const span=document.createElement('span');span.className='word';span.dataset.index=++index;span.textContent=match[0];$('text').append(span);end=match.index+match[0].length;
  }
  $('text').append(document.createTextNode(story.text.slice(end)));highlight(0);
}
function highlight(position){
  const spans=[...$('text').querySelectorAll('.word')];
  const confirmed=Number.isInteger(position)?Math.max(0,Math.min(position,spans.length)):0;
  const size=(session?.guide_words??Number($('guide').value))===2?2:1;
  const next=confirmed<spans.length?confirmed+1:null;
  const end=next===null?null:Math.min(spans.length,next+size-1);
  for(const span of spans){
    const n=+span.dataset.index;span.className='word'+(n<=confirmed?' past':'')+(n===confirmed?' recognized':'')+(next!==null&&n>=next&&n<=end?' current':'');
    if(next!==null&&n===confirmed+1)span.setAttribute('aria-current','step');else span.removeAttribute('aria-current');
  }
  $('position').textContent=next?(size===2?`Bloque: «${spans.slice(next-1,end).map(s=>s.textContent).join(' ')}» · ${next}–${end}/${spans.length}`:`Siguiente: «${spans[next-1].textContent}» · ${next}/${spans.length}`):'Se ha reconocido el final del texto';
  $('heard').textContent=confirmed?`Última reconocida: «${spans[confirmed-1].textContent}»`:'Empieza por la palabra resaltada';
}
async function refresh(){
  try{const s=await request('/api/status');if(active)return;
    $('start').disabled=s.state!=='ready'||s.model!==$('model').value;$('prepare').disabled=s.state==='loading';
    note(s.state==='loading'?'Preparando el modelo en la CPU del ordenador…':s.state==='ready'?(s.model!==$('model').value?'Pulsa «Preparar modelo» para cargar el reconocedor seleccionado.':`${cfg.models[s.model]||s.model} preparado · CPU local${s.rss_mib?` · RAM actual ${(s.rss_mib/1024).toFixed(2)} GiB`:''}`):s.error||'Prepara un modelo para empezar.');
  }catch(e){note(e.message);$('start').disabled=true;}
}
function snapshot(){
  const length=Math.min(total,ring.length),start=(cursor-length+ring.length)%ring.length,output=new Float32Array(length);
  const first=Math.min(length,ring.length-start);output.set(ring.subarray(start,start+first));
  if(first<length)output.set(ring.subarray(0,length-first),first);return output;
}
function maybeSend(){if(active&&!stopping&&!busy&&session&&total-lastSent>=context.sampleRate*session.requested_step_seconds)inflight=sendWindow().catch(()=>{});}
async function sendWindow(force=false){
  if(busy||!session||!total||(!force&&total-lastSent<context.sampleRate*session.requested_step_seconds))return;
  busy=true;const end=total/context.sampleRate,pcm=snapshot();lastSent=total;const sent=performance.now();
  try{
    const r=await request(`/api/audio?id=${session.id}&rate=${context.sampleRate}&end=${end}`,pcm.buffer,true,pendingRender?{'X-Lexia-Render':JSON.stringify(pendingRender)}:{});
    highlight(r.position);$('asr').textContent=r.hypothesis||'(sin palabras reconocidas)';$('infer').textContent=r.asr_wall_seconds.toFixed(2)+' s';
    const render=performance.now(),age=render-(firstPerf+end*1000);$('age').textContent=(age/1000).toFixed(2)+' s';
    pendingRender={id:session.id,kind:'render',index:r.index,request_roundtrip_ms:render-sent,estimated_cut_age_at_render_ms:age};
    note(active?'Micrófono activo · lee a tu ritmo':'Terminando y guardando registro…');
  }catch(e){note('Problema: '+e.message);throw e;}finally{busy=false;setTimeout(maybeSend,0);}
}
function consume(chunk){
  if(!active)return;for(const value of chunk){ring[cursor]=value;cursor=(cursor+1)%ring.length;}total+=chunk.length;
  if(firstPerf===null)firstPerf=performance.now()-total/context.sampleRate*1000;
  if($('keep').checked)saved.push(chunk.slice());
  let sum=0;for(const x of chunk)sum+=x*x;$('level').value=Math.sqrt(sum/chunk.length);$('elapsed').textContent=(total/context.sampleRate).toFixed(1)+' s';
  if(total/context.sampleRate>=600){stop();return;}
  maybeSend();
}
async function release(){if(stream)stream.getTracks().forEach(t=>t.stop());if(node)node.disconnect();if(source)source.disconnect();if(gain)gain.disconnect();}
async function start(){
  $('start').disabled=true;for(const id of ['prepare','model','story','keep','window','step','guide'])$(id).disabled=true;
  try{
    if(!navigator.mediaDevices?.getUserMedia||!window.AudioWorkletNode)throw new Error('Usa Chrome en localhost con acceso al micrófono.');
    stream=await navigator.mediaDevices.getUserMedia({audio:{channelCount:1,echoCancellation:false,noiseSuppression:false,autoGainControl:false},video:false});
    context=new AudioContext({sampleRate:16000});await context.resume();await context.audioWorklet.addModule('/capture.js');
    session=await request('/api/start',{story:$('story').value,window:Number($('window').value),step:Number($('step').value),client_profile:2,guide_words:Number($('guide').value)});
    $('configuration').textContent=`Ventana de hasta ${session.window_seconds} s; actualización solicitada cada ${session.requested_step_seconds} s.`;
    const settings=stream.getAudioTracks()[0].getSettings();await request('/api/event',{id:session.id,kind:'capture',settings});
    $('settings').textContent=`Captura: ${context.sampleRate} Hz; ajustes reales del micrófono: ${JSON.stringify({echoCancellation:settings.echoCancellation,noiseSuppression:settings.noiseSuppression,autoGainControl:settings.autoGainControl})}`;
    ring=new Float32Array(context.sampleRate*session.window_seconds);cursor=total=lastSent=0;firstPerf=null;saved=[];busy=false;stopping=false;pendingRender=null;draw();
    if(wavURL)URL.revokeObjectURL(wavURL);$('download').hidden=true;$('saved').textContent='';
    node=new AudioWorkletNode(context,'lexia-capture');node.port.onmessage=e=>{if(e.data.flushed){if(flushResolve)flushResolve();}else consume(e.data);};
    source=context.createMediaStreamSource(stream);gain=context.createGain();gain.gain.value=0;
    active=true;source.connect(node);node.connect(gain);gain.connect(context.destination);$('stop').disabled=false;note('Micrófono activo · empieza a leer.');
  }catch(e){active=false;await release();if(context)await context.close();if(session){await request('/api/event',{id:session.id,kind:'finish'}).catch(()=>{});session=null;}note(e.message);unlock();}
}
function unlock(){for(const id of ['prepare','model','story','keep','window','step','guide'])$(id).disabled=false;$('stop').disabled=true;$('start').disabled=false;}
function wav(){
  const length=saved.reduce((n,a)=>n+a.length,0),data=new ArrayBuffer(44+length*2),v=new DataView(data);let offset=44;
  const text=(o,s)=>{for(let i=0;i<s.length;i++)v.setUint8(o+i,s.charCodeAt(i));};
  text(0,'RIFF');v.setUint32(4,36+length*2,true);text(8,'WAVE');text(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,context.sampleRate,true);v.setUint32(28,context.sampleRate*2,true);v.setUint16(32,2,true);v.setUint16(34,16,true);text(36,'data');v.setUint32(40,length*2,true);
  for(const part of saved)for(const x of part){v.setInt16(offset,Math.round(Math.max(-1,Math.min(1,x))*32767),true);offset+=2;}
  wavURL=URL.createObjectURL(new Blob([data],{type:'audio/wav'}));$('download').href=wavURL;$('download').download=`Lectura en directo - ${$('story').value.replace('.txt','')} - ${new Date().toISOString().slice(0,10)} - lector_sin_asignar.wav`;$('download').hidden=false;
}
async function stop(){
  if(!active||stopping)return;stopping=true;$('stop').disabled=true;
  const flushed=new Promise(resolve=>{flushResolve=resolve;});node.port.postMessage('flush');
  await Promise.race([flushed,new Promise(resolve=>setTimeout(resolve,300))]);active=false;await release();
  try{await inflight;if(total>lastSent)await sendWindow(true);if($('keep').checked&&saved.length)wav();
    const r=await request('/api/event',{id:session.id,kind:'finish',render:pendingRender});$('saved').textContent='Registro local: '+r.file;note('Lectura terminada. Puedes repetir o cambiar de modelo.');
  }catch(e){await request('/api/event',{id:session.id,kind:'finish'}).catch(()=>{});note('Lectura terminada con incidencia: '+e.message);}
  finally{if(context)await context.close();session=null;unlock();}
}
window.addEventListener('beforeunload',()=>{
  if(stream)stream.getTracks().forEach(t=>t.stop());
  if(session&&cfg)fetch('/api/event',{method:'POST',headers:{'X-Lexia-Token':cfg.token,'Content-Type':'application/json'},body:JSON.stringify({id:session.id,kind:'finish',render:pendingRender}),keepalive:true});
});
async function init(){
  cfg=await request('/api/config');for(const s of cfg.stories){const o=document.createElement('option');o.value=s.id;o.textContent=s.id.replace('.txt','');$('story').append(o);}
  for(const [key,name] of Object.entries(cfg.models)){const o=document.createElement('option');o.value=key;o.textContent=name;$('model').append(o);}
  $('model').value=cfg.runtime.model||'granite_turboctc';draw();$('story').onchange=draw;$('guide').onchange=draw;$('model').onchange=refresh;$('start').onclick=start;$('stop').onclick=stop;
  $('prepare').onclick=async()=>{try{await request('/api/prepare',{model:$('model').value});await refresh();}catch(e){note(e.message);}};
  await refresh();setInterval(refresh,2000);
}
init().catch(e=>note(e.message));
