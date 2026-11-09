# MLS dev · coste secuencial frente a concurrente

Revisión del 06/11/2026. Cuatro motores, mismos 100 IDs/FLAC/referencias: 1493.21 s de audio. Crisper excluido. Los 400 resultados nuevos y los 400 originales correspondientes se recalculan desde las transcripciones. SHA256 de descarga, firmas, modelos/parámetros/versiones, cobertura y conteos JSONL verificados; 100 huellas locales cotejadas. Originales conservados. Sin ASR nuevo ni escucha humana independiente.

## Reconocimiento: mismos 100 audios

| Motor | ASR concurrente s | ASR secuencial s | Cambio % | WER concurrente % | WER secuencial % | Textos distintos (normalizados) |
|---|---:|---:|---:|---:|---:|---:|
| xlsr | 12.33 | 12.30 | -0.27 | 10.02 | 10.02 | 0 (0) |
| parakeet | 24.90 | 20.44 | -17.92 | 6.04 | 6.04 | 0 (0) |
| whisper | 54.54 | 50.29 | -7.79 | 8.43 | 8.43 | 0 (0) |
| vosk | 137.09 | 103.11 | -24.79 | 13.99 | 13.99 | 0 (0) |

Un cambio negativo de tiempo indica menor tiempo secuencial. WER es error de palabras: menor es mejor. No se compara el tiempo de 100 audios con el de 2.408 ni con el WER del corpus completo. Las diferencias de texto y sus referencias se conservan en comparacion.json.

## Recursos durante el tramo de los 100 audios

| Motor | RAM RSS máx. concurrente / secuencial MiB | VRAM PID máx. concurrente / secuencial MiB | Potencia GPU media concurrente / secuencial W |
|---|---:|---:|---:|
| xlsr | 4152.7 / 4158.7 | 3112.0 / 3112.0 | 91.5 / 107.4 |
| parakeet | 4604.5 / 4615.8 | 4024.0 / 4024.0 | 56.1 / 69.9 |
| whisper | 3192.0 / 3203.5 | 1970.0 / 1970.0 | 104.0 / 111.2 |
| vosk | 223.0 / 220.1 | n/d / n/d | n/d / n/d |

Tramo desde el inicio del primer audio hasta el final del último, con los huecos de puntuación/escritura entre ambos. Excluye carga y calentamiento; los pesos residentes siguen contando. Máximos muestreados, no picos garantizados. Potencia media aritmética de muestras de la GPU física, no consumo exclusivo o neto del ASR; Vosk no usa GPU.

## Inicialización y sesión secuencial

| Motor | Carga/importación s | Calentamiento s | Sesión instrumentada s | RTF ASR |
|---|---:|---:|---:|---:|
| xlsr | 53.21 | 25.83 | 101.79 | 0.0082 |
| parakeet | 11.89 | 6.25 | 46.02 | 0.0137 |
| whisper | 5.33 | 25.61 | 86.63 | 0.0337 |
| vosk | 0.73 | 1.26 | 106.87 | 0.0691 |

## Resultado observado

Las 400 hipótesis nuevas son idénticas carácter a carácter a sus 400 salidas previas: se conserva WER/CER. El tiempo ASR disminuye 17,92 % en Parakeet, 7,79 % en Whisper y 24,79 % en Vosk; XLSR cambia solo −0,27 %. RAM RSS y VRAM del tramo comparable permanecen próximas; no se demuestra un ahorro importante de memoria al ejecutar cada modelo por separado. No se detectan otros procesos de cómputo en las muestras de la GPU seleccionada durante estos tramos.

Carga/calentamiento de XLSR (53,21/25,83 s) y Whisper (5,33/25,61 s) son mayores que en el lote anterior; estos costes no desaparecen aunque el ASR caliente sea más rápido. Sin repeticiones o control del resto del servidor no se identifica la causa. La potencia media GPU muestreada es mayor en los tramos nuevos, lo que tampoco implica por sí solo mayor energía neta por audio.

## Interpretación

- La secuencia temporal confirma que no se solapan nuestros cuatro procesos. El servidor continúa compartido: otros usuarios pueden usar CPU/RAM/disco. La etiqueta aislada describe esta cohorte, no exclusividad del servidor.
- Una sola pasada por condición. No atribuir todas las diferencias a eliminar concurrencia: cambian fecha, cachés, estado del sistema y GPU física (Parakeet pasa de 1 a 0; Whisper de 2 a 0). Revisar GPU/hardware y muestras, sin prometer significación estadística.
- La calidad no debería asumirse idéntica: comprobar textos distintos. Decodificación numérica y empates pueden variar; no se establece una causa de cambios sin pruebas adicionales.
- Los tiempos de carga/calentamiento y escritura son distintos de ASR. Estos costes siguen guardados; diferencias en la duración de sesión no son necesariamente mejoras del reconocedor.
- Esta prueba mide reconocimiento offline, no el seguidor, latencia visual o rendimiento de tablet. Test permanece reservado.

## Cambios de transcripción

### xlsr

Ningún texto distinto.

### parakeet

Ningún texto distinto.

### whisper

Ningún texto distinto.

### vosk

Ningún texto distinto.

