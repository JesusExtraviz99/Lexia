# Segundo cuento: velocidades, relectura, disfluencias y ruido

23/10/2026. Lote exploratorio de siete WAV nuevos del mismo adulto, texto lectura_02.txt. Ventanas acústicas 4 y 8 s, actualización cada 2 s, tres rondas de cómputo por WAV, mismo modelo small CPU int8, VAD y seguidor habitual. Las reglas experimentales de palabra aislada, filtro temporal y recuperación exacta no se activan durante estas inferencias. Cada comparación guarda recursos disponibles y simulación de cola. No cambiar reglas mientras se procesa el lote.

## Contenido comunicado por el lector

El usuario confirma que terminó todos los cuentos. No comunica ruido de fondo en estas lecturas, excepto la prueba de ruido, donde reproduce desde el móvil sonidos de una calle. Esto describe las condiciones percibidas; no es una medida de SNR ni ausencia acústica absoluta de ruido.

| Consigna / nombre | Duración del WAV | Referencia disponible |
|---|---:|---|
| Lectura lenta | 90 s | Cuento terminado; ritmo según nombre. |
| Lectura rápida | 30 s | Cuento terminado; ritmo según nombre. |
| Pausa con relectura | 50 s | Lee «Junto a una fuente descubrió un pequeño barco rojo», pausa aproximada de 8 s y repite esa misma frase; después continúa hasta el final. |
| Sustitución rojo por azul | 50 s | Sustitución según nombre; cuento terminado. |
| Ruido de fondo | 50 s | Sonido de calle reproducido desde un móvil; cuento terminado. |
| Muchas trabadas | 60 s | Fragmentos y repeticiones a lo largo de la lectura, por ejemplo «Una ta ta tarde, Lu, Lucía…», hasta el final. La lista literal completa no está anotada. |
| Omisión de abuelo | 40 s | El lector confirma que omitió ambas apariciones de abuelo, en «con su abuelo» y «Su abuelo la ayudó»; cuento terminado. |

No convertir títulos o estos ejemplos en una transcripción literal completa. Se necesitará escucha/revisión de los tramos para atribuir diferencias al lector o al ASR. La relectura vuelve aproximadamente de la posición 19 a la 11 y luego continúa; objetivo final del cuento: 56, estantería. Las consignas con rojo por azul y omisión no implican por sí mismas que el seguidor deba retroceder.

## Ejecución y revisión por el usuario

El lote iniciado por el asistente está en resultados/lotes/20261023_102114_072901. Dentro hay un lote.json con selección por fecha, cuento y SHA256, una carpeta por audio con seis ejecuciones y sus fichas de recursos, y un log por audio. resumen.md reúne los resultados cuando el lote termina. Solo se incluyen los siete WAV presentes cuyas huellas coinciden, no entradas históricas sin un WAV coincidente.

Para ver avance sin repetir las inferencias, desde la carpeta del proyecto:

```powershell
Get-Content .\resultados\lotes\20261023_102114_072901\lote.json -Raw -Encoding UTF8 | ConvertFrom-Json | Select-Object -ExpandProperty recordings | Select-Object label,status
```

Para leer el resumen al terminar:

```powershell
Get-Content .\resultados\lotes\20261023_102114_072901\resumen.md -Encoding UTF8
```

Para repetir el lote en otra ocasión (crea otra carpeta; no ejecutar mientras el actual está en marcha):

```powershell
.\.venv\Scripts\python.exe -u -m scripts.comparar_lote --fecha 2026-10-23 --cuento .\datos\textos\lectura_02.txt --ventanas 4 8 --repeticiones 3
```

Las tres rondas repiten inferencia sobre el mismo WAV; no son lecturas independientes. Alcanzar 56 no prueba seguimiento correcto durante todo el cuento, detección de disfluencias ni precisión temporal. Sin marcas humanas no se calculará latencia real del subrayado ni WER contra el cuento como si fuera transcripción de las lecturas con errores. No publicar sin revisión compartida.

## Resultados de la primera revisión del asistente

Lote completo: 42 ejecuciones y 1.110 actualizaciones, con integridad de los siete WAV y el cuento comprobada. Todas las posiciones finales son 56 y las trayectorias se repiten entre las tres rondas de cada configuración; los textos ASR no son idénticos en todas las rondas de lenta 4 s y trabadas 4/8 s. Esto no equivale a nuevas lecturas ni a una referencia de precisión.

La ventana de 4 s tiene menor total medio de inferencia en los siete WAV. Sin embargo, en lenta presenta un máximo de 9,18 s frente a 2,43 s con 8 s; en trabadas ambas tienen máximos superiores a 11 s. Una ventana corta no garantiza menor pico ni ausencia de cola. La duración incluye silencio final y llamadas muy baratas del VAD, por lo que no se identifica una ventana ganadora solo con el total.

En pausa/relectura, las seis ejecuciones mantienen 19 durante la pausa y retroceden de 19 a 13 en el corte 20 s; después vuelven a 19 y continúan hasta 56. Es una relectura local, no el caso anterior de recuperación lejana después de terminar el cuento. En sustitución, ambas ventanas conservan azul en sus hipótesis y continúan; en omisión no aparece abuelo en ninguna hipótesis de las seis ejecuciones. Son observaciones del texto ASR y la trayectoria, no un detector automático ya validado de errores lectores.

En trabadas, las primeras hipótesis incluyen fragmentos/repeticiones y cambian al aumentar el contexto. En primera ronda, la posición empieza a fijarse en corte 6 s con 4 s y 8 s con 8 s; sin anclas humanas no son demoras respecto a la palabra real. Prioridad de revisión compartida: escuchar el inicio y algunos tramos de trabadas, comparándolos con las hipótesis, y después las dos omisiones y la relectura. No ajustar reglas antes de cerrar esa revisión.

La revisión detallada está en resultados/lotes/20261023_102114_072901/revision_asistente.md y .json; este último conserva las huellas de los 42 registros. Los recursos están en cada comparación. Pasan 67 pruebas de software; las funciones Tracker, locate y audio_bounds coinciden por AST con 30c4c83. No se publica ni activa ninguna regla experimental.

## Revisión cualitativa de trabadas completada

23/10/2026. El lector revisa 0–8, 16–24, 34–42 y 48–56 s, ronda 1, y marca simplificación en ambas ventanas en los cuatro fragmentos. Deja notas con intentos y repeticiones escuchados. Se verifican audio, fuentes y cuatro estados revisados. La referencia está en datos/anotaciones/lectura_02_trabadas_revision_cualitativa.json y el resumen en resultados/lotes/20261023_102114_072901/revision_humana_trabadas.md/.json. No es transcripción literal exhaustiva ni tiempos de palabras; no permite calcular tasa global de detección ni generalizar a todas las trabadas. El avance hasta 56 coexiste con pérdida parcial de fragmentos y repeticiones del ASR. No se elige ventana ganadora por estas valoraciones. Mantener reglas; próximo contraste: omisiones y pausa/relectura sobre los registros existentes.
