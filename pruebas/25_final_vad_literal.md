# Primer ensayo de control VAD del final

25/10/2026. El usuario autoriza probar el límite final de entrada en los seis audios señalados y dos controles. Ensayo de desarrollo offline, sin activar un cambio del seguidor habitual.

## Diseño y procedencia

Fuente: resultados/literalidad/20261025_182446_557677_UTC. Casos problemáticos originales 1, 4, 5, 6, 11, 17; controles 9 (normal del cuento 2) y 16 (muchas trabadas). Se mantiene esa numeración en nombres e informes; el nuevo selector tiene ocho casos.

La condición original es la salida literal previamente medida, reutilizada con su SHA256. No se reejecuta el motor habitual ni se inventa un baseline nuevo. La variante ejecuta ocho inferencias nuevas con el mismo candidato, versiones, trabajador y diccionario de parámetros comprobados. Modelo Small CPU float32/Transformers, cuatro hilos, modo verbatim, protecciones y continuación larga conservadas. No se cambian palabras, prompts, penalizaciones, temperaturas o filtro de ruido.

Único tratamiento de entrada: se conserva el array desde la muestra cero hasta el último final de voz VAD detectado con margen ya incluido. Se reutiliza el diagnóstico VAD anterior, fijado por huella: threshold 0,5, min_speech_duration_ms 0, min_silence_duration_ms 2000, speech_pad_ms 400. No se añade otro margen de 400 ms ni se usan las marcas humanas para elegir el final. No se concatenan trozos de voz ni se eliminan pausas internas. El original y una copia de escucha completa permanecen disponibles para evaluar silencios y errores.

Los ocho originales suman 480 s; la entrada nueva, 341,12 s. Las 66 anclas humanas disponibles en estos casos quedan dentro de los prefijos enviados. Esto no valida sílabas sin marcas ni demuestra sensibilidad del VAD en todos los eventos. Acortar la duración cambia algunos bloques y puede activar la ruta corta en entradas de hasta 30 s: es una comparación de canalización, no aislamiento de una causa interna de alucinación. No es seguimiento en directo ni usa audio futuro para ese seguidor, que no se modifica.

## Resultado observado

Carpeta: resultados/literalidad/20261025_193651_692690_cola_vad_UTC. Completadas ocho salidas nuevas. Se verifica byte a byte que cada texto nuevo es un prefijo exacto del anterior: los únicos cambios textuales son los siguientes sufijos retirados.

| Audio | Cambio textual respecto al literal original |
|---|---|
| 1 | Se retira la continuación «Vas por el lado de las chicas…» y las repeticiones de «las mariposas». |
| 4 | Se retira «Ven». Persisten «desváceo» y «jugador no». |
| 5 | Se retira «Ven». Persiste la omisión de «a» en «llamó a su hermano». La relectura real se conserva. |
| 6 | Se retira «¿Y por qué no se puede ver el maravilla?». La relectura completa se conserva. |
| 9, control normal | Texto completo idéntico. |
| 11 | Se retira «A la vez de hoy, la familia está en su casa, y el joven se lo lleva». |
| 16, control de trabadas | Texto completo idéntico, incluidos los intentos ya reconocidos y la omisión de «re-» señalada anteriormente. |
| 17 | Texto completo idéntico: siguen «Consu» y «Suu», sin restaurar «abuelo». |

Son cinco añadidos finales conocidos retirados en cinco casos seleccionados; no es una precisión del 100 %, una garantía de ausencia de otros errores o una prueba independiente. La comparación textual demuestra que no cambió el resto de lo escrito en estos ocho casos, no que el texto reconocido contenga todos los intentos reales. Las nuevas salidas permanecen pendientes de escucha compartida.

## Recursos e integridad

Inferencia previa reutilizada para estos casos: 287,48 s; inferencia nueva: 87,95 s. Carga única nueva: 11,62 s; pico de RAM de la vida del proceso nuevo: 4.451,94 MiB. CPU por audio, máximos muestreados de RAM y GPU global están en candidato.json y metricas.json. La inferencia nueva suma 352,98 s de CPU acumulada. La RAM del modelo sigue siendo elevada; acortar la cola no demuestra una reducción importante de sus pesos o una implementación viable en tablet.

Los tiempos anteriores provienen de un proceso de 17 casos, los nuevos de uno de ocho; orden, temperatura y caché pueden influir. El VAD se midió antes y sus resultados se reutilizan; no está incluido como coste nuevo en 87,95 s. No es una medición pareada repetida ni tiempo total de una aplicación. RTF sobre duración original y sobre duración enviada se guardan separados. Ambos ensayos usan CPU; GPU global no equivale a consumo del ASR.

integridad.json verifica ocho prefijos exactos, fuentes anteriores intactas, modelo, parámetros/versiones/trabajador idénticos y 66 anclas conservadas. Se conserva la fuente ejecutada, la preparación y el generador de informes. Las 83 pruebas del proyecto pasan antes de las inferencias. Los originales y las salidas previas no se reescriben. Los timestamps automáticos y avisos de compatibilidad del candidato mantienen sus límites anteriores.

## Revisión desde el ordenador del lector

Visor: http://127.0.0.1:8778/. Dos paneles claramente identificados: literal original del lote anterior y literal con final VAD nuevo. El audio reproduce por defecto el original completo; el selector de escucha permite oír exactamente el prefijo enviado. Revisar los añadidos retirados y las últimas palabras/intententos, sin confundir una relectura real con una alucinación. El visor no guarda valoraciones ni ejecuta ASR.

Comprobación sin nuevas transcripciones:

```powershell
.\.venv\Scripts\python.exe -m scripts.probar_final_vad_literal verificar resultados/literalidad/20261025_193651_692690_cola_vad_UTC
Get-Content .\resultados\literalidad\20261025_193651_692690_cola_vad_UTC\resumen.md -Encoding UTF8
```

Para abrir el visor si está cerrado:

```powershell
.\.venv\Scripts\python.exe -m scripts.ver_piloto_literal resultados/literalidad/20261025_193651_692690_cola_vad_UTC --puerto 8778
```

Para reproducir el contraste en una carpeta nueva:

```powershell
$ensayoVAD = .\.venv\Scripts\python.exe -m scripts.probar_final_vad_literal preparar resultados/literalidad/20261025_182446_557677_UTC --fecha 2026-10-25 | Select-Object -Last 1
.\.tools\literal-env\Scripts\python.exe -u -m scripts.comparar_literalidad candidato "$ensayoVAD"
.\.venv\Scripts\python.exe -m scripts.probar_final_vad_literal resumir "$ensayoVAD"
.\.venv\Scripts\python.exe -m scripts.probar_final_vad_literal verificar "$ensayoVAD"
```

No se adopta una regla de borrar todo lo posterior al cuento ni una lista negra de frases: el límite depende del audio detectado, conservando relecturas posteriores. Siguiente decisión tras escucha: ampliar el contraste al resto de casos y después a audios nuevos, sin atribuir aún las mejoras a un mecanismo interno concreto. Sin publicación automática.

## Ampliación: los dos controles de pausa larga

**Controles adicionales de pausa larga.** A raíz de la pregunta del usuario se aclara que 3/13 no estaban en la primera tanda y se realizan dos inferencias nuevas con la misma variante, resultados/literalidad/20261025_195038_565692_cola_vad_UTC. Se conservan muestra a muestra las pausas interiores; en 3, flor 11,88→Ana 21,20 s delimita 9,32 s íntegros y tres anclas retenidas. En 13 se conserva la relectura dos veces y el texto completo es idéntico; sus ~8 s son descripción/consigna, sin medida humana precisa. En 3 solo desaparece la etiqueta [throatclearing], sin adjudicarla como correcta o errónea; persisten errores lexicales previos. Entrada 110→73,152 s; inferencia previa/nueva 38,98/21,21 s, carga nueva 7,91 s; 85 pruebas pasan antes de inferir. control_pausas.md/validacion_pausas.json e integridad conservan comprobaciones; visor 8779. Es análisis offline que usa la última voz del archivo, no validación de cierre automático de sesión en directo. Actualización en la misma E060, sin activar ni publicar.

La selección adicional se prepara con --audios 3 13. Los ocho resultados anteriores y sus salidas originales se conservan.
