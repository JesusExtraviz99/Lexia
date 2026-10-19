"use strict";
const $ = id => document.getElementById(id);
let data, draft, nonce, selected = 0, dirty = false, samples, peaksMin, peaksMax, duration = 40;
let viewStart = 0, viewEnd = 8, segment = null, loop = false;
const audio = $("audio");
const fmt = n => n.toFixed(2).replace(".", ",");
function status(message, error = false) { $("status").textContent = message; $("status").classList.toggle("error", error); }
function markDirty() { dirty = true; $("save").disabled = false; status("Cambios pendientes de guardar."); }
function word() { return data.words[selected]; }
function renderWords() {
  $("words").replaceChildren();
  data.words.forEach((w, i) => {
    const b = document.createElement("button");
    b.className = "word" + (w.reviewed ? " done" : w.start !== null ? " timed" : "") + (i === selected ? " selected" : "");
    b.setAttribute("aria-pressed", String(i === selected));
    b.setAttribute("aria-label", `${w.index}. ${w.word}, ${w.reviewed ? "revisada" : w.start !== null ? "tiempos pendientes de revisión" : "sin tiempos"}`);
    const n = document.createElement("small"); n.textContent = w.index;
    b.append(n, document.createTextNode(w.word + (w.reviewed ? " ✓" : "")));
    b.addEventListener("click", () => select(i)); $("words").append(b);
  });
  const total = data.words.filter(w => w.reviewed).length;
  $("progress").textContent = `${total}/${data.words.length} revisadas · primera frase ${data.words.slice(0, 9).filter(w => w.reviewed).length}/9`;
}
function renderEditor() {
  const w = word(); $("word-title").textContent = `${w.index}. ${w.word}`;
  $("start").value = w.start === null ? "" : w.start.toFixed(2);
  $("end").value = w.end === null ? "" : w.end.toFixed(2);
  $("reviewed").checked = w.reviewed; $("note").value = w.note;
  $("origin").textContent = `Origen: ${w.timing_origin.replaceAll("_", " ")} · ${w.reviewed ? "declarada revisada por escucha" : "pendiente de revisión"}`;
  $("previous").disabled = selected === 0; $("next").disabled = selected === data.words.length - 1;
}
function select(i) { segment = null; audio.pause(); selected = i; focusWord(); renderWords(); renderEditor(); drawAll(); }
function focusWord() {
  const w = word(); const t = w.start ?? audio.currentTime;
  viewStart = Math.max(0, t - 1); viewEnd = Math.min(duration, Math.max(viewStart + 5, (w.end ?? t) + 1));
  if (viewEnd - viewStart < 3) viewStart = Math.max(0, viewEnd - 5);
}
function draw(canvas, start, end) {
  const width = Math.max(200, canvas.clientWidth), height = canvas.clientHeight;
  const ratio = window.devicePixelRatio || 1; canvas.width = width * ratio; canvas.height = height * ratio;
  const ctx = canvas.getContext("2d"); ctx.scale(ratio, ratio);
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  const scaleX = t => (t - start) / (end - start) * width;
  if (data) {
    const w = word();
    if (w.start !== null && w.end !== null) {ctx.fillStyle = dark ? "#477c604d" : "#17695e26"; ctx.fillRect(scaleX(w.start), 0, scaleX(w.end) - scaleX(w.start), height);}
  }
  if (samples) {
    ctx.strokeStyle = dark ? "#a4ccba" : "#356d5a"; ctx.lineWidth = 1; ctx.beginPath();
    for (let x = 0; x < width; x++) {
      const a = Math.floor((start + x / width * (end - start)) / duration * samples.length);
      const b = Math.min(samples.length, Math.max(a+1, Math.floor((start + (x+1) / width * (end-start)) / duration * samples.length)));
      let min = 0, max = 0;
      for (let p = a; p < b; p++) {min = Math.min(min, peaksMin[p]); max = Math.max(max, peaksMax[p]);}
      ctx.moveTo(x, height/2 - max * (height/2 - 16)); ctx.lineTo(x, height/2 - min * (height/2 - 16));
    }
    ctx.stroke();
  }
  ctx.fillStyle = dark ? "#c2d6ca" : "#314f42"; ctx.font = "12px Segoe UI";
  for (let t = Math.ceil(start); t <= end; t += Math.max(1, Math.ceil((end-start)/8))) ctx.fillText(`${t}s`, Math.min(width-25, scaleX(t)+2), height-5);
  if (audio.currentTime >= start && audio.currentTime <= end) {ctx.strokeStyle = "#c27026";ctx.beginPath();ctx.moveTo(scaleX(audio.currentTime),0);ctx.lineTo(scaleX(audio.currentTime),height);ctx.stroke();}
}
function drawAll() { draw($("overview"),0,duration); draw($("detail"),viewStart,viewEnd); $("window-label").textContent = `Fragmento ampliado: ${fmt(viewStart)}–${fmt(viewEnd)} s`; }
function editTimes(start, end) {
  const w = word(); w.start = start; w.end = end; w.reviewed = false;
  w.timing_origin = w.timing_origin.startsWith("borrador_asr") || w.timing_origin === "asr_ajustado" ? "asr_ajustado" : "manual";
  markDirty(); renderEditor(); renderWords(); drawAll();
}
function currentInputs() { return [$("start").value === "" ? null : Number($("start").value), $("end").value === "" ? null : Number($("end").value)]; }
function validWord(w) {return Number.isFinite(w.start) && Number.isFinite(w.end) && w.start >= 0 && w.end > w.start && w.end <= duration;}
$("start").addEventListener("change", () => editTimes(...currentInputs()));
$("end").addEventListener("change", () => editTimes(...currentInputs()));
$("note").addEventListener("input", () => {word().note = $("note").value; markDirty();});
$("reviewed").addEventListener("change", () => {
  if ($("reviewed").checked && !validWord(word())) {$("reviewed").checked=false;status("Ajusta primero un intervalo válido para esta palabra.",true);return;}
  word().reviewed = $("reviewed").checked; markDirty(); renderWords(); renderEditor();
});
$("draft").addEventListener("click", () => {
  if (!draft) return;
  if (data.words.some(w => w.start !== null) && !confirm("Esto sustituirá los tiempos y desmarcará todas las revisiones. ¿Cargar el borrador ASR?")) return;
  data.words = structuredClone(draft.words); markDirty(); select(0);
  $("draft-status").textContent = "Tiempos ASR cargados. Ninguna palabra está revisada todavía.";
});
$("previous").addEventListener("click", () => select(Math.max(0,selected-1)));
$("next").addEventListener("click", () => select(Math.min(data.words.length-1,selected+1)));
$("focus").addEventListener("click", () => {focusWord();drawAll();});
$("speed").addEventListener("change", () => audio.playbackRate = Number($("speed").value));
$("loop").addEventListener("click", () => {loop=!loop;$("loop").textContent=`Repetir: ${loop?"sí":"no"}`;$("loop").setAttribute("aria-pressed",String(loop));});
$("mark-start").addEventListener("click", () => editTimes(Number(audio.currentTime.toFixed(2)),word().end));
$("mark-end").addEventListener("click", () => editTimes(word().start,Number(audio.currentTime.toFixed(2))));
$("play").addEventListener("click", async () => {
  if (!validWord(word())) {status("Indica inicio y fin, o carga el borrador ASR.",true);return;}
  const context=Number($("context").value);segment={start:Math.max(0,word().start-context),end:Math.min(duration,word().end+context)};
  audio.currentTime=segment.start; await audio.play();
});
audio.addEventListener("play", () => { if (samples) requestAnimationFrame(tick); });
function tick() {
  if (segment && audio.currentTime >= segment.end) {if(loop){audio.currentTime=segment.start;}else{audio.pause();audio.currentTime=segment.end;segment=null;}}
  $("clock").textContent=`${fmt(audio.currentTime)} s`;drawAll(); if(!audio.paused) requestAnimationFrame(tick);
}
audio.addEventListener("seeked", () => {$("clock").textContent=`${fmt(audio.currentTime)} s`;drawAll();});
$("overview").addEventListener("click", e => {
  const rect=e.currentTarget.getBoundingClientRect();const t=Math.max(0,Math.min(duration,(e.clientX-rect.left)/rect.width*duration));
  segment=null;audio.pause();audio.currentTime=t;viewStart=Math.max(0,t-2);viewEnd=Math.min(duration,viewStart+6);drawAll();
});
$("detail").addEventListener("click", e => {
  const rect=e.currentTarget.getBoundingClientRect();const t=Number((viewStart+(e.clientX-rect.left)/rect.width*(viewEnd-viewStart)).toFixed(2));
  editTimes(e.shiftKey?word().start:t,e.shiftKey?t:word().end);
});
$("save").addEventListener("click", async () => {
  $("save").disabled=true;
  try {
    const res=await fetch("/api/guardar",{method:"POST",headers:{"Content-Type":"application/json","X-Anotador-Token":nonce},body:JSON.stringify(data)});
    const result=await res.json();if(!res.ok)throw new Error(result.error||"No se pudo guardar.");
    data=result.annotation;dirty=false;renderWords();renderEditor();status(`Guardado: ${data.reviewed_words}/${data.words.length} palabras revisadas. Puedes cerrar y retomar después.`);
  } catch(e) {$("save").disabled=false;status(e.message,true);}
});
window.addEventListener("beforeunload", e => {if(dirty){e.preventDefault();e.returnValue="";}});
window.addEventListener("resize", () => {if(data)drawAll();});
async function init() {
  try {
    const res=await fetch("/api/caso");const loaded=await res.json();if(!res.ok)throw new Error(loaded.error);
    data=loaded.annotation;draft=loaded.asr_draft;nonce=loaded.nonce;duration=data.duration_seconds;
    $("draft").disabled=!draft;$("draft-status").textContent=draft?"Borrador ASR disponible; cargarlo es opcional. Solo la escucha valida los tiempos.":"Marca los tiempos manualmente.";
    renderWords();renderEditor();drawAll();
    status(data.saved_at_utc?"Progreso anterior recuperado. Continúa donde lo dejaste.":"Listo. Selecciona una palabra o carga el borrador ASR para empezar.");
    const buffer=await (await fetch("/audio")).arrayBuffer();
    const context=new AudioContext();const decoded=await context.decodeAudioData(buffer);const raw=decoded.getChannelData(0);
    const bins=Math.min(12000,raw.length);peaksMin=new Float32Array(bins);peaksMax=new Float32Array(bins);
    for(let i=0;i<bins;i++){const a=Math.floor(i/bins*raw.length),b=Math.floor((i+1)/bins*raw.length);for(let k=a;k<b;k++){peaksMin[i]=Math.min(peaksMin[i],raw[k]);peaksMax[i]=Math.max(peaksMax[i],raw[k]);}}
    samples=peaksMin;await context.close();drawAll();
  } catch(e) {status(`No se pudo preparar el reproductor: ${e.message}`,true);}
}
init();
