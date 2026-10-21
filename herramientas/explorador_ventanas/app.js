"use strict";
const $=id=>document.getElementById(id);
let data, index=15;
const players=[];
const num=n=>n.toFixed(2).replace('.',',');
const names={original:'Original',combinada:'Combinación anterior',nueva:'Recuperación exacta nueva'};
const modes={local:'Búsqueda local',recuperacion_pendiente:'Recuperación pendiente de confirmación',recuperacion:'Recuperación confirmada',hipotesis_sin_cambios:'Texto idéntico: no se vuelve a procesar',recuperacion_global_exacta:'Frase exacta: recuperación directa',retroceso_sin_tiempo_nuevo:'Retroceso rechazado: tiempo antiguo',palabra_aislada_consecutiva:'Avance por palabra aislada'};
function node(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
function pauseAll(){players.forEach(p=>p.pause());}
function wave(canvas,row,color){
 const width=canvas.getBoundingClientRect().width||500,height=120,ratio=devicePixelRatio||1;
 canvas.width=width*ratio;canvas.height=height*ratio;const c=canvas.getContext('2d');c.scale(ratio,ratio);
 const x=t=>t/data.duration*width;c.fillStyle='#bbc4d0';c.fillRect(0,0,x(row.start),height);
 c.fillStyle='#eef0f3';c.fillRect(x(row.end),0,width-x(row.end),height);
 c.fillStyle=color+'22';c.fillRect(x(row.start),0,x(row.end-row.start),height);
 data.peaks.forEach((p,i)=>{const t=i*.05;c.strokeStyle=t>=row.start&&t<row.end?color:'#8492a4';c.beginPath();c.moveTo(x(t),60-p*52);c.lineTo(x(t),60+p*52);c.stroke();});
 c.strokeStyle=color;c.lineWidth=2;c.strokeRect(x(row.start),1,Math.max(1,x(row.end-row.start)),118);
 c.fillStyle='#203047';c.font='12px Segoe UI';c.fillText(`${row.start.toFixed(0)}–${row.end.toFixed(0)} s`,Math.min(width-65,Math.max(5,x(row.start))),16);
}
function explanation(row){
 const o=row.variants.original,n=row.variants.nueva,g=row.global_candidate_diagnostic;
 const parts=[];
 if(o.mode==='hipotesis_sin_cambios')parts.push('El texto es idéntico al corte anterior. El original no lo usa como una confirmación adicional.');
 else if(o.mode==='recuperacion_pendiente')parts.push(`La búsqueda global propone ${g}, pero el original espera otro candidato igual en una actualización procesada.`);
 else if(o.mode==='recuperacion')parts.push('El original confirma el candidato global pendiente y acepta el regreso.');
 else if(o.evidence.position==null)parts.push('La hipótesis no aporta una coincidencia local suficiente. El original conserva su posición mientras intenta recuperarse.');
 else parts.push(`El original encuentra apoyo local en ${o.position}: ${o.word}.`);
 if(n.mode==='recuperacion_global_exacta')parts.push(`La regla nueva acepta ahora una frase exacta única con tiempos posteriores y vuelve a ${n.position}: ${n.word}.`);
 else if(n.position!==o.position)parts.push(`La nueva variante ya está en ${n.position}: ${n.word}; conserva o continúa la recuperación anterior.`);
 return parts.join(' ');
}
function render(){
 pauseAll();players.length=0;$('panels').replaceChildren();const round=Number($('round').value);
 const runs=data.runs.filter(r=>r.repeat===round).sort((a,b)=>a.window-b.window);
 const end=runs[0].rows[index].end;$('cutlabel').textContent=`Corte: ${num(end)} s`;$('cut').value=index;
 $('prev').disabled=index===0;$('next').disabled=index===runs[0].rows.length-1;
 for(const run of runs){
  const row=run.rows[index],panel=node('section',undefined,`panel window${run.window}`);
  const h=node('h2',`Ventana de ${run.window} segundos`);h.append(node('span',`${num(row.start)} → ${num(row.end)} s`,'badge'));panel.append(h);
  const canvas=node('canvas');canvas.setAttribute('role','img');canvas.setAttribute('aria-label',`Audio recibido entre ${row.start} y ${row.end} segundos sobre la grabación completa.`);panel.append(canvas);
  const labels=node('div',undefined,'timeline-labels');labels.append(node('span','0 s'),node('span',`${data.duration} s · grabación completa`));panel.append(labels);
  const listen=node('button',`▶ Escuchar solo ${num(row.start)}–${num(row.end)} s`,'listen');panel.append(listen);
  const audio=node('audio');audio.controls=true;audio.preload='none';audio.src=row.clip;audio.playbackRate=Number($('rate').value);audio.loop=$('loop').checked;panel.append(audio);players.push(audio);
  audio.addEventListener('play',()=>players.forEach(p=>{if(p!==audio)p.pause();}));
  listen.addEventListener('click',async()=>{pauseAll();audio.currentTime=0;try{await audio.play();}catch(e){$('status').textContent='No se pudo reproducir: '+e.message;}});
  panel.append(node('span','TRANSCRIPCIÓN GUARDADA','sectionlabel'));
  const transcript=node('div',undefined,'transcript');row.hypothesis.forEach((w,i)=>{transcript.append(node(i>=row.hypothesis.length-8?'mark':'span',w),document.createTextNode(' '));});
  if(!row.hypothesis.length)transcript.textContent='Sin palabras reconocidas.';panel.append(transcript,node('p','Resaltado: últimas 8 palabras usadas por el alineador.','muted'));
  for(const [key,v] of Object.entries(row.variants)){const box=node('div',undefined,'decision');box.append(node('strong',`${names[key]} · ${v.position??'—'}${v.word?' · '+v.word:''}`),node('small',modes[v.mode]||v.mode));panel.append(box);}
  panel.append(node('p',explanation(row),'explain'),node('p',`Inferencia guardada: ${num(row.processing)} s · Salida lista simulada: ${num(row.ready)} s. El corte de audio es ${num(row.end)} s.`,'muted'));
  $('panels').append(panel);wave(canvas,row,run.window===4?'#137e8c':'#65519c');
 }
 $('status').textContent='Listo. Solo consulta y escucha; no modifica tus resultados ni vuelve a ejecutar el ASR.';
}
$('cut').addEventListener('input',e=>{index=Number(e.target.value);render();});
$('prev').onclick=()=>{index--;render();};$('next').onclick=()=>{index++;render();};$('round').onchange=render;
$('rate').onchange=()=>players.forEach(p=>p.playbackRate=Number($('rate').value));$('loop').onchange=()=>players.forEach(p=>p.loop=$('loop').checked);
document.querySelectorAll('[data-cut]').forEach(b=>b.onclick=()=>{index=data.runs[0].rows.findIndex(r=>r.end===Number(b.dataset.cut));render();});
window.addEventListener('resize',()=>{if(data)render();});
fetch('/data').then(r=>{if(!r.ok)throw Error('No se pudieron cargar los datos.');return r.json();}).then(d=>{
 data=d;const rounds=[...new Set(d.runs.map(r=>r.repeat))].sort();rounds.forEach(r=>{const o=node('option',String(r));o.value=r;$('round').append(o);});
 $('cut').max=d.runs[0].rows.length-1;index=Math.min(index,d.runs[0].rows.length-1);$('file').textContent=d.audio;render();
}).catch(e=>{$('status').textContent='Error: '+e.message;});
