# Piloto separado de transcripción literal

23/10/2026. Objetivo: comprobar si una rama distinta del seguidor conserva intentos y repeticiones que el ASR actual simplifica. No se activa en producción ni se obtienen automáticamente estadísticas de disfluencias.

## Selección y procedencia

Siete recortes de 8 s: cuatro muestras revisadas de la lectura con trabadas del segundo cuento (0–8, 16–24, 34–42, 48–56), dos controles de lectura fluida del primer cuento con referencia validada por el lector (0–8 y 8–16), y un control sin habla con ruidos ambientales leves (30–38 del mismo WAV normal). Son dos WAV del mismo adulto, no siete lecturas ni una muestra independiente. La referencia de ausencia de habla es la confirmación del lector después del cuento, no VAD usado como verdad. Las notas de trabadas no son una transcripción exhaustiva por evento.

Faster Whisper Small, CTranslate2 CPU int8, y CrisperWhisper 2.0 Small, Transformers CPU float32; cuatro hilos por motor, sin VAD, sin cuento ni notas como prompt. Una pasada por motor, mismo array remuestreado a 16 kHz. Candidato: modo verbatim, límites de generación y mitigación de bucles predeterminados explícitos; word_timestamps activado en ambos, sin validación humana de los tiempos del candidato. Procesos separados, modelo compartido dentro de cada proceso.

Entorno principal intacto. Entorno adicional: .tools/literal-env, Python 3.12.15, crisperwhisper 2.0.3, torch 2.14.1+cpu, transformers 5.20.2. Modelo público nyralabs/CrisperWhisper2.0_small fijado a bcaecf0a584a1f600d8897fe6032b9e2e56429a7, con huellas de 13 archivos, token de español comprobado y licencia de investigación no comercial registrada en sus archivos. Consultar el modelo/licencia antes de decidir un despliegue; aquí solo se ensaya investigación local. No se envió audio a un servicio externo.

## Resultados exploratorios

Salida: resultados/literalidad/20261023_124047_726452. En inicio, el modelo actual produce «Una tarde Lucía paseaba por el parque» y el candidato «U- u- una tarde lu- lucia pa- paseaba por el par- parque». El candidato también escribe «Descu- descubrió», «pe- pequeño», «ori- o- orilla», «la la ayudó», «y y» y «lo y lo colocaron». Son indicios de mayor conservación frente al baseline y compatibles parcialmente con las notas, pendientes de revisión de eventos y de su número/forma exactos.

La salida de Intermedio 1 contiene «el el barco, el barco rojo». Tras escuchar el recorte 16–24 s, el lector confirma que la última aparición de «el barco rojo» no se pronuncia: se registra como inserción del ASR, no como repetición recuperada. La causa (anticipación o repetición generada) no queda determinada. Confirmación parcial separada, con huellas de entrada y salida, en datos/anotaciones/lectura_02_piloto_literal_revision.json; no equivale a validar toda la transcripción. En el control fluido 8–16, el candidato añade «Los dos» frente al baseline; la referencia humana sitúa Los en 15,46–15,77 y dos en 15,78–16,10, por lo que el recorte sí contiene parte de ese tramo. Reconocer una palabra antes de completarse no prueba invención ni precisión temporal. Ambos motores devuelven vacío en el control sin habla. No se observan nuevas repeticiones en los dos textos de control fluido, sin que eso demuestre ausencia de falsos positivos en general.

| Implementación | Inferencia total (56 s de entrada) | Carga | Pico RAM del proceso durante su vida |
|---|---:|---:|---:|
| Actual · CT2 int8 | 14,08 s | 1,15 s | 696,73 MiB |
| Candidato · Transformers float32 | 50,37 s | 18,33 s | 4.252,89 MiB |

El pico incluye importaciones/carga/buffers/ejecución. Las implementaciones difieren en backend y precisión; no atribuir toda la diferencia al modelo ni predecir tablet. Datos completos de CPU/RAM y GPU global disponibles por proceso en baseline.json/candidato.json. No se ha medido energía específica del ASR. Queda pendiente optimización y medición móvil si se adopta una rama de análisis.

Compatibilidad registrada: el cargador avisa de dos tensores encoder_blank_head inesperados y de opciones de generación/atención deprecadas o potencialmente ignoradas con esta versión de Transformers. No se han aplicado parches al paquete ni eliminado pesos. La prueba valida que produce texto; sus marcas automáticas de palabra no se presentan como tiempos precisos validados. Resolver/validar esa compatibilidad antes de basar estadísticas de duración en ellas.

## Comprobación compartida

Visor local de solo lectura: http://127.0.0.1:8775/. Seleccionar cada muestra, escuchar y comparar texto actual, candidato y notas. No guarda valoraciones ni modifica referencias. Intermedio 1 ya tiene confirmación puntual del lector: la frase final extra es una inserción. Queda revisar los demás eventos para cuantificar fidelidad. La confirmación se conserva separada de las hipótesis originales. No calcular precisión/F1 por evento a partir de cuatro juicios globales.

Verificación sin inferencias:

```powershell
.\.venv\Scripts\python.exe -m scripts.verificar_piloto_literal resultados/literalidad/20261023_124047_726452
```

Para reabrir el visor, si su servidor está cerrado:

```powershell
.\.venv\Scripts\python.exe -m scripts.ver_piloto_literal resultados/literalidad/20261023_124047_726452 --puerto 8775
```

Para repetir en una carpeta nueva, sin sobreescribir las fuentes anteriores:

```powershell
$pilotoLiteral = .\.venv\Scripts\python.exe -m scripts.comparar_literalidad preparar | Select-Object -Last 1
.\.venv\Scripts\python.exe -u -m scripts.comparar_literalidad baseline "$pilotoLiteral"
.\.tools\literal-env\Scripts\python.exe -u -m scripts.comparar_literalidad candidato "$pilotoLiteral"
.\.venv\Scripts\python.exe -m scripts.comparar_literalidad resumir "$pilotoLiteral"
.\.venv\Scripts\python.exe -m scripts.verificar_piloto_literal "$pilotoLiteral"
```

Scripts secuenciales; no repetir mientras otro reconocimiento está en marcha. No modificar audio, modelo o notas entre motores. El manifiesto fija fuentes, arrays y procedencia; las copias de escucha se guardan en .descartados, ignorado por Git. El verificador conserva huellas de outputs y, cuando coincide, fuente exacta ejecutada. Las inferencias completas rechazan sobrescritura.

## Decisión provisional

La separación de ramas permite ensayar un reconocedor más literal conservando el seguimiento. El candidato es prometedor, pero aún no es referencia ni motor elegido: confirmar fidelidad, definir episodios e intentos revisados, comprobar falsos positivos y medir coste/compatibilidad. No cambiar reglas del seguidor ni sumar hipótesis solapadas como eventos. Sin publicación automática.

## Contraste posterior con la grabación completa

A petición del lector, se procesa el WAV entero de 60 s con ambos motores: resultados/literalidad/20261023_131712_130708. Los cuatro arrays previos coinciden exactamente con sus intervalos en el array completo; se conservan los parámetros cortos y se registran los valores predeterminados de continuación larga. El candidato divide internamente en 0–30, 26–56 y 52–60 s, con contexto generado. No es una única ventana de 60 s ni una prueba de seguimiento en directo.

La frase añadida al final de Intermedio 1 ya no aparece como tal: el candidato continúa «el el barco el barco flotaba…». Esto muestra sensibilidad a la entrada/contexto en esta ejecución, sin aislar la causa ni validar todos los intentos. El bloque inicial ahora incluye audio hasta 30 s, frente al corte previo a 24 s. Los demás eventos siguen pendientes de revisión literal del lector. Informe reproducible: comparacion_contexto.md dentro de esa carpeta; visor http://127.0.0.1:8776/ con audio completo y cuatro recortes previos.

Inferencia actual/candidato: 5,23/15,50 s; carga 1,00/7,44 s; pico RAM 696,68/4.417,32 MiB. RTF 0,087/0,258 sobre los 60 s, incluido silencio final; no es demora en directo ni rendimiento en tablet. Se conservan CPU/RAM/GPU global y versiones. Avisos de cargador/generación documentados; marcas de palabra no validadas. El usuario autoriza publicar ambas pruebas y las novedades del proyecto en GitHub; la publicación conserva el estado exploratorio y no activa el motor en el seguidor.

```powershell
$completo = .\.venv\Scripts\python.exe -m scripts.comparar_literalidad preparar_completo resultados/literalidad/20261023_124047_726452 | Select-Object -Last 1
.\.venv\Scripts\python.exe -u -m scripts.comparar_literalidad baseline "$completo"
.\.tools\literal-env\Scripts\python.exe -u -m scripts.comparar_literalidad candidato "$completo"
.\.venv\Scripts\python.exe -m scripts.comparar_literalidad resumir "$completo"
.\.venv\Scripts\python.exe -m scripts.verificar_piloto_literal "$completo"
.\.venv\Scripts\python.exe -m scripts.informar_literalidad_completa "$completo"
```

Fuentes primarias: [modelo](https://huggingface.co/nyralabs/CrisperWhisper2.0_small), [documentación del autor](https://github.com/nyrahealth/CrisperWhisper/blob/main/DOCS.md), contrastadas con el paquete instalado y el checkpoint fijado. Las afirmaciones de rendimiento del autor no sustituyen este piloto propio.

**Revisión del audio completo por el lector.** El lector completa la escucha y valora el resto como bastante fiel; señala una omisión de intento: se oye «regres- re- regresaron» y el candidato escribe «regres- regresaron». Es un episodio conservado parcialmente, con tres intentos humanos (dos parciales y la palabra completa) frente a dos escritos; falta «re-». Confirmación con huellas en datos/anotaciones/lectura_02_literal_completa_revision.json, sin tiempos humanos interiores ni anotación exhaustiva por evento. No se calcula un porcentaje global de precisión. Las salidas ASR originales permanecen intactas; no se ejecuta reconocimiento nuevo.
