'use strict';
const $=id=>document.getElementById(id);
const flagLabels={fragmentos:'Intentos incompletos',silabas_repetidas:'Sílabas repetidas',palabras_repetidas:'Palabras repetidas',reinicios:'Vuelve a empezar',sin_trabadas:'Sin trabadas en este fragmento',dudoso:'No lo distingo con claridad'};
const choices=[['','Elegir…'],['conserva','Conserva las trabadas que oigo'],['simplifica','Simplifica o elimina trabadas'],['cambia','Cambia palabras o fragmentos'],['mixto','Combina varios comportamientos'],['dudoso','No puedo decidir']];
let data,index=0,dirty=false;
function stopAudio(){document.querySelectorAll('audio').forEach(a=>a.pause());}
function playback(){document.querySelectorAll('audio').forEach(a=>{a.playbackRate=Number($('rate').value);a.loop=$('loop').checked;});}
function markDirty(){dirty=true;$('status').textContent='Cambios sin guardar.';}
function collect(){if(!data)return;const r=data.annotation.reviews[index];r.heard=[...$('flags').querySelectorAll('input:checked')].map(a=>a.value);r.asr4=$('asr4').value;r.asr8=$('asr8').value;r.notes=$('notes').value;r.reviewed=$('reviewed').checked;}
function element(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
function renderPanels(){
  stopAudio();const section=data.sections[index];const cut=section.cuts[Number($('cut').value)];$('panels').replaceChildren();
  for(const w of cut.windows){const p=element('article',undefined,'panel');p.append(element('h3',`Ventana de ${w.seconds} segundos`),element('p',`Audio ${w.start.toFixed(1)}–${w.end.toFixed(1)} s`));const audio=document.createElement('audio');audio.controls=true;audio.preload='metadata';audio.src=w.clip;p.append(audio,element('p',w.text||'(Sin texto reconocido)','transcript'),element('p',`Posición: ${w.position??'sin fijar'} · ${w.word||'—'} | Inferencia: ${w.processing.toFixed(2)} s`,'position'));$('panels').append(p);}
  playback();
}
function render(){
  stopAudio();const s=data.sections[index],r=data.annotation.reviews[index];$('title').textContent=s.title;$('interval').textContent=`Fragmento ${s.start}–${s.end} segundos`;$('progress').textContent=`${index+1} de ${data.sections.length} · ${data.annotation.reviews.filter(a=>a.reviewed).length} marcados revisados`;$('prev').disabled=index===0;$('next').disabled=index===data.sections.length-1;$('context').src=s.clip;$('comparison').hidden=true;$('reveal').hidden=false;
  $('cut').replaceChildren();s.cuts.forEach((cut,i)=>{const o=element('option',`${cut.end} s`);o.value=i;$('cut').append(o);});$('cut').value=s.cuts.length-1;
  $('flags').replaceChildren();for(const [value,text] of Object.entries(flagLabels)){const label=document.createElement('label');const input=document.createElement('input');input.type='checkbox';input.value=value;input.checked=r.heard.includes(value);label.append(input,document.createTextNode(' '+text));$('flags').append(label);}
  for(const id of ['asr4','asr8']){const select=$(id);select.replaceChildren();choices.forEach(([value,text])=>{const o=element('option',text);o.value=value;select.append(o);});select.value=r[id];}
  $('notes').value=r.notes;$('reviewed').checked=r.reviewed;renderPanels();
}
async function save(){
  collect();$('save').disabled=true;$('status').textContent='Guardando…';
  try{const response=await fetch('/api/guardar',{method:'POST',headers:{'Content-Type':'application/json','X-Revision-Token':data.nonce},body:JSON.stringify({reviews:data.annotation.reviews})});const result=await response.json();if(!response.ok)throw Error(result.error||'No se pudo guardar.');data.annotation=result.annotation;dirty=false;const n=data.annotation.reviews.filter(r=>r.reviewed).length;$('status').textContent=`Guardado localmente. ${n} de 4 fragmentos revisados.`;$('progress').textContent=`${index+1} de 4 · ${n} marcados revisados`;}
  catch(error){$('status').textContent='No se ha guardado: '+error.message;}
  finally{$('save').disabled=false;}
}
$('prev').onclick=()=>{collect();index--;render();};$('next').onclick=()=>{collect();index++;render();};$('rate').onchange=playback;$('loop').onchange=playback;$('cut').onchange=renderPanels;$('reveal').onclick=()=>{$('comparison').hidden=false;$('reveal').hidden=true;};$('save').onclick=save;
for(const id of ['flags','asr4','asr8','notes','reviewed'])$(id).addEventListener('input',markDirty);
document.addEventListener('play',event=>{if(event.target.tagName==='AUDIO')document.querySelectorAll('audio').forEach(a=>{if(a!==event.target)a.pause();});},true);
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
fetch('/api/revision').then(async response=>{const result=await response.json();if(!response.ok)throw Error(result.error);return result;}).then(result=>{data=result;$('file').textContent=data.audio_label;$('destination').textContent='Archivo de revisión: '+data.annotation_file;render();$('status').textContent='Escucha y guarda tus observaciones. Puedes guardar aunque queden fragmentos pendientes.';}).catch(error=>{$('status').textContent='No se pudo cargar: '+error.message;});
