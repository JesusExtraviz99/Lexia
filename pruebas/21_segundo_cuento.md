# Segundo cuento: contraste sin ajustar reglas

21/10/2026. Lectura normal confirmada y comparación de variantes comprobada por ambas partes. Relectura todavía pendiente.

## Texto y condiciones

Texto original creado para la prueba: datos/textos/lectura_02.txt, 56 palabras. Mantener mismo adulto, micrófono, equipo, modelo small CPU int8, VAD, bloques de 2 s y ventanas 4/8 s. Tres rondas de cómputo por grabación, no tres lecturas. Registrar ruido real comunicado, sin asumir lluvia constante ni condiciones idénticas entre días. No añadir filtros de ruido o cambiar umbrales durante estas dos pruebas. No se fija aún una ventana ganadora.

## Caso 1: lectura normal

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 40 --cuento .\datos\textos\lectura_02.txt
```

Leer el cuento completo una sola vez, ritmo natural, sin comentarios y después silencio. No activar el micrófono por cuenta del asistente: el programa espera Enter del usuario. Objetivo final 56, estantería, y conservación del final. No declarar referencia literal ni tiempos humanos hasta confirmación del lector.

Tras recibir la ruta concreta:

```powershell
.\.venv\Scripts\python.exe -u scripts\comparar_ventanas.py RUTA_DEL_WAV --cuento .\datos\textos\lectura_02.txt --ventanas 4 8 --repeticiones 3
```

El parámetro --cuento es necesario: el valor predeterminado sigue siendo lectura_01.txt. El manifiesto guarda ruta y hash del cuento. El comparador de seguidores reutiliza story_words de cada registro, sin inferencias nuevas.

## Caso 2: relectura (después de revisar el caso normal)

Leer el cuento completo, pausa aproximada de dos segundos y repetir lentamente solo Junto a una fuente descubrió un pequeño barco rojo. Terminar en rojo, no continuar El barco. Duración prevista 60 s, confirmar contenido y duración reales. Objetivo: regreso de 56 (estantería) a 19 (rojo); tramo releído 11–19. No se afirma de antemano que la nueva regla deba activarse o ser mejor. La pausa de la consigna no constituye una marca temporal.

Comparar original, combinación y recuperación exacta usando idénticas hipótesis, sin ajustar reglas para favorecer resultados. Para medir demora usar anclas selectivas revisadas si son necesarias; distinguir identificación parcial de palabra completa. Si no recupera, conservar el fallo y diagnosticarlo sin modificar el umbral antes de cerrar esta primera comparación.

## Versiones fijadas antes de grabar

Cuento SHA256: 0c78d65f0d4ecff05998f596c1917135db529bf74bc4a2776a9a809d2e1c4c0b

```json
{
  "seguir.py": "57a49bca80d23b8a1fb3ab2654dac5f410aba2fd0dff4640f877b0bee6179e2e",
  "comparar_seguidores.py": "1882749d1fc116f98e4b06e1eb6ab08fa531fe0ca78ec6c69cdf15cd6481e887",
  "comparar_recuperacion.py": "039e05a47e1ea27613386392e84f8befa2af4ba13409eb07967549b92804f5e9"
}
```

Este contraste amplía texto manteniendo el lector. Dos grabaciones nuevas no validan generalización clínica/infantil ni todas las condiciones de ruido. Una vez revisadas ambas, podrán formar parte del conjunto fijo de audios para comparar otros reconocedores. No publicar automáticamente.

## Primera lectura normal recibida

WAV lectura_20261021_110858_556291.wav, 40 s. El usuario informa de lluvia. Máximo 1,0: una muestra PCM16 al límite, sin racha prolongada; no permite por sí sola valorar distorsión audible. Fuente ASR resultados/comparaciones/20261021_111057_752726. Cuento/hash comprobados y reglas idénticas a las fijadas antes de grabar.

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_relectura_lejana resultados/comparaciones/20261021_111057_752726 --control-sin-relectura
```

Ejecución del asistente resultados/controles_sin_relectura/20261021_111428_479787: todas las posiciones coinciden entre versiones, sin retrocesos ni activaciones de la recuperación exacta; final 56 en corte 26 y conservado. El usuario confirma la lectura y comparte resultados/controles_sin_relectura/20261021_111600_102761. Los seis registros completos coinciden con el asistente; control revisado conjuntamente. No se calcula precisión lexical ni demora sin referencia humana. Inferencias >2 s: 18/60 en ventana 4 y 11/60 en 8; cola máxima 2,07 y 2,27 s. No se identifica una causa de los cambios de coste. No modificar reglas antes de cerrar el segundo caso previsto.

## Integridad del guardado

seguir.py y comparar_ventanas.py guardan JSON/informes mediante temporal y sustitución del destino, con reintentos limitados de errores de escritura/acceso. Esto modifica el archivo seguir.py respecto a su hash inicial, pero no las reglas: se verifica por AST que audio_bounds, locate y Tracker son idénticos a la versión publicada. comparar_seguidores.py y comparar_recuperacion.py permanecen intactos. Las ejecuciones incompletas se conservan y no se tratan como comparaciones completas. La repetición crea una carpeta independiente; no se combinan sus tiempos con la parcial. Este cambio es de fiabilidad de los registros, sin ajuste de reconocimiento ni del seguidor.

## Relectura completa recibida

El usuario confirma cuento correcto y repetición lenta. WAV lectura_20261021_114202_408281.wav, 45 s, nivel máximo comunicado 0,8402. Ejecución completa resultados/comparaciones/20261021_115105_998651: seis registros de 23 cortes hasta 45 s, cuento/hash comprobados. No mezclar sus tiempos con ejecuciones parciales. Referencia de contenido datos/referencias/lectura_02_relectura.json; anclas humanas pendientes.

```powershell
.\.venv\Scripts\python.exe -m scripts.comparar_relectura_lejana resultados/comparaciones/20261021_115105_998651
```

Comparación del asistente resultados/relectura_lejana/20261021_115740_472120: nueva 4 s recupera 19 en corte 40, original/combinación final 56; nueva 8 s vuelve a 16 en 36, 17 en 38 y 19 en 40, original/combinación recuperan 19 en 42. Repetido en tres rondas. En ventana 4 s/corte 30 aparecen textos que el usuario confirma no haber pronunciado (despedidas de vídeo y Hum); no cambian la posición 56 de ninguna versión en ese corte. La causa acústica no se establece. El usuario comparte resultados/relectura_lejana/20261021_115941_383989: seis registros completos coincidentes con el asistente. Se prepara el anotador --caso relectura_cuento_02 para estantería, Junto y rojo, sin tiempos propuestos. Marcas humanas pendientes; no cambiar reglas para favorecer el resultado.

## Contraste temporal de la relectura

Anclas revisadas por el usuario: estantería 25,25–26,13 s, Junto 29,25–30,13 y rojo 38,81–39,95. Nota en rojo: Ruido de fondo algo notable. La nota no demuestra que el ruido cause las hipótesis inventadas.

```powershell
.\.venv\Scripts\python.exe -m scripts.evaluar_relectura_lejana resultados/relectura_lejana/20261021_115941_383989 --caso relectura_cuento_02
```

Salida lista en rojo desde el final humano: nueva 4 s media 1,85 s, nueva 8 s 1,65, original/combinación 8 s 3,69; original/combinación 4 s sin recuperación. Todos estos cortes ya incluyen el final humano de rojo, no hay identificación parcial previa como en azul. La nueva 8 s vuelve a un durante la relectura y llega a rojo en corte 40; la nueva 4 s recupera directamente a rojo en 40. Tiempos de salida simulados, sin pantalla ni coste extra de variantes. Primera evaluación del asistente; pendiente de contraste compartido.
