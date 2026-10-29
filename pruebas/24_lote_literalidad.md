# Lote de transcripción completa de los audios propios

**Fecha:** 25/10/2026. Comparación de desarrollo solicitada por el usuario: pasar el reconocedor literal por todos los audios disponibles antes de elegir los siguientes casos de revisión.

## Entradas y diseño

17 WAV propios presentes en datos/audio, 880 s (14 min 40 s), dos cuentos y un lector adulto. Se verifican las huellas del catálogo y su cobertura exacta de los WAV: no se omiten archivos sin avisar ni se procesa como otro audio una entrada histórica sin contenido coincidente. El dataset externo todavía no está en el proyecto; no se incluye.

Cada WAV se reconoce entero una vez por motor. No se reutilizan las hipótesis cortas o el piloto anterior como si fueran estas inferencias nuevas. Ambos reciben el mismo array mono float32 de 16 kHz, decodificado sin limpieza de ruido ni VAD. El cuento, las notas y los eventos descritos no se entregan al reconocedor. Se conservan los WAV originales, una copia de escucha PCM16 y huellas del array. El catálogo se congela en una copia del manifiesto; los JSON de resultados y anotaciones anteriores se verifican al finalizar.

Motor actual de comparación: Faster Whisper Small, CTranslate2, CPU int8, cuatro hilos, español, beam 5, marcas automáticas de palabra, sin VAD ni condicionamiento entre segmentos. Candidato: CrisperWhisper 2.0 Small, revisión bcaecf0a584a1f600d8897fe6032b9e2e56429a7, Transformers CPU float32, cuatro hilos, español, modo verbatim, máximo 256 tokens por bloque, mitigación de repeticiones y temperaturas alternativas activadas. Son los ajustes del piloto; no una búsqueda de parámetros óptimos.

Para entradas mayores de 30 s, el candidato usa continuation, bloques de 30 s/paso 26 s, 12 palabras de contexto generado, retirada temporal de hasta dos palabras y recuperación de cierre temprano. Los bloques efectivos quedan en native_result.chunks. No escucha una grabación entera de 90 s en una sola ventana. Esta prueba es offline y no cambia el seguidor habitual ni evalúa latencia visual.

## Recursos, procedencia y resultados

Carpeta del lote: resultados/literalidad/20261025_182446_557677_UTC. Un proceso por motor y modelo reutilizado en los 17 audios, orden del catálogo idéntico, motores secuenciales. Se registran tiempos de carga única, inferencia/CPU/RTF por audio, muestras de RAM y GPU global por intervalo, y métricas de amplitud de la entrada decodificada. Una sola pasada: no mide variabilidad entre rondas, nuevas voces ni datos de prueba reservados.

RAM por audio: máximo muestreado en su intervalo y extremos, no pico independiente garantizado; el proceso puede conservar memoria de audios anteriores. El pico Windows pertenece a toda la vida del proceso, incluida la carga. CPU acumulada puede superar el tiempo de pared por los hilos. Las muestras globales de GPU/VRAM/potencia/temperatura no son consumo atribuible al ASR: ambos motores ejecutan en CPU. Sin energía propia del ASR, FLOPs o medidas de tablet. RTF sobre audio total, incluido silencio; no RTF sobre habla ni demora del seguidor. Decodificar a 16 kHz y reproducir PCM16 introduce diferencias de representación documentadas; los dos motores reciben exactamente el mismo array.

Archivos: manifest.json (WAV/arrays/modelos/catálogo/fuentes previas), baseline.json y candidato.json (salidas brutas y recursos), sus logs, fuente_ejecutada.txt y fuente_lote.txt, resumen.md, metricas.json e integridad.json. Los modelos/entornos/cachés y el diario alternativo permanecen fuera de Git.

Persisten las advertencias de compatibilidad del candidato documentadas en el piloto: encoder_blank_head, atención/generación, límites de tokens y tokenización. Las marcas de palabras no se convierten en tiempos humanos sin validarlas. No se corrigen a mano las salidas brutas ni se cuentan automáticamente sus repeticiones como disfluencias reales.

## Reproducir y revisar

Preparar otro lote conserva las ejecuciones anteriores. Los comandos de inferencia rechazan sobrescribir un resultado existente. Ejecutar los motores secuencialmente.

```powershell
$loteLiteral = .\.venv\Scripts\python.exe -m scripts.lote_literalidad preparar --fecha 2026-10-25 | Select-Object -Last 1
.\.venv\Scripts\python.exe -u -m scripts.comparar_literalidad baseline "$loteLiteral"
.\.tools\literal-env\Scripts\python.exe -u -m scripts.comparar_literalidad candidato "$loteLiteral"
.\.venv\Scripts\python.exe -m scripts.lote_literalidad resumir "$loteLiteral"
.\.venv\Scripts\python.exe -m scripts.lote_literalidad verificar "$loteLiteral"
.\.venv\Scripts\python.exe -m scripts.ver_piloto_literal "$loteLiteral" --puerto 8777
```

El visor permite elegir el WAV por su nombre descriptivo, escucharlo completo con controles de velocidad y comparar ambos textos y recursos. No graba, no lanza inferencias ni guarda valoraciones humanas. Estas salidas nuevas requieren revisión; las confirmaciones anteriores describen su audio o ejecuciones concretas y no validan automáticamente este lote.

La comparación debe distinguir episodios reales recuperados, intentos omitidos dentro de un episodio, palabras pronunciadas que el motor sustituye y texto añadido sin apoyo audible. Una diferencia entre motores no determina cuál acierta. WER literal, precisión/F1, conteos, pausas o duraciones humanas requieren referencias compatibles; no se deducen del cuento pretendido ni de los timestamps automáticos sin validar. Los controles normales y los silencios sirven para buscar falsos positivos. No se cambian reglas ni se publica el lote sin petición del usuario.

## Cierre técnico

**Resultado del lote.** Completadas 34 transcripciones (17 por motor), sin nuevas inferencias por ventanas. Inferencia total actual/candidato 131,50/426,57 s para 880 s de entrada; carga única 2,17/18,91 s; pico RAM de la vida del proceso 980,84/4.466,64 MiB. RTF total 0,149/0,485, con silencio. Verificados los 17 WAV/arrays, archivos de ambos modelos, fuente exacta ejecutada y 693 fuentes previas intactas. El candidato conserva Ana repetida, mar- mariposa y azul, y no restaura abuelo, pero deforma contexto y añade texto en el final sin habla de la primera lectura normal; el actual añade Suscríbete en la segunda normal y el literal no. La lenta del primer cuento pierde cuaderno en la salida literal. En muchas trabadas el texto coincide con el ensayo anterior y conserva la omisión de re- ya señalada por el lector. No se atribuyen estos contrastes a una causa única ni se calculan tasas globales sin referencia por evento. Resumen, métricas e integridad separados y observaciones.md documentan evidencia y límites; visor http://127.0.0.1:8777/ para revisión de todas las salidas. Candidato y ajustes habituales del seguidor permanecen separados; sin publicación automática.
