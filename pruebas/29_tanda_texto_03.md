# Texto 3: El tren y el pañuelo verde

26/10/2026. Primera tanda prevista para datos/textos/lectura_03.txt, conservado sin modificaciones. Doce tomas, con tres controles de ritmo y fenómenos de dificultad creciente. Un adulto; simulación exploratoria de desarrollo, no validación clínica o independiente. Consignas estructuradas en lectura_03_tomas.json. El texto contiene dos apariciones legítimas de El tren llegó a la estación: la repetición textual del cuento no es por sí misma una disfluencia o relectura adicional.

## Grabar

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --plan datos/textos/lectura_03_tomas.json
```

Enter inicia la toma, otro Enter la termina y guarda; la siguiente espera una nueva pulsación. Duración real en WAV y catálogo, sin rellenar el resto con silencio. Los tiempos son límites de seguridad, no esperas obligatorias. Puedes dejar un breve margen tras la última palabra. Ctrl+C interrumpe, no guarda anticipadamente. Nombres reales Tren 01–12 con cuento/fecha; conservar micrófono y distancia y comunicar condiciones reales. No presumir silencio porque no se haya añadido ruido.

| Toma | Máximo (s) | Fenómeno previsto |
|---|---:|---|
| 01 | 90 | Normal, ambas apariciones legítimas de El tren... |
| 02 | 180 | Lenta sin errores deliberados. |
| 03 | 90 | Rápida e inteligible. |
| 04 | 120 | Tren, Clara y pañuelo repetidos. |
| 05 | 150 | Intentos en pequeña, regresaron y ventanilla. |
| 06 | 90 | Omisiones de primer y verde. |
| 07 | 120 | Rojo→verde y abuelo→abuela con autocorrección explícita. |
| 08 | 150 | Pausa aproximada de 12 s antes de la segunda llegada del tren. |
| 09 | 150 | Cuento entero y vuelta a las tres primeras frases; termina en andén. |
| 10 | 150 | Frase de Su hermano... andén omitida y recuperada después de ventanilla. |
| 11 | 120 | Carraspeo entre frases, separado de errores léxicos. |
| 12 | 180 | Mezcla difícil libre y descripción posterior. |

Máximos acumulados 1.590 s (26 min 30 s); la parada manual permite duraciones menores. No tratar el máximo como tiempo realmente leído. Las tres velocidades no son tres rondas del mismo audio: son nuevas capturas. Las consignas no sustituyen las referencias por escucha ni aseguran ausencia de errores no previstos.

Para consultar sin activar el micrófono, añadir --listar. Para dividir la tanda o retomarla:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --plan datos/textos/lectura_03_tomas.json --hasta 6
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --plan datos/textos/lectura_03_tomas.json --desde 7
```

No repetir la primera mitad si ya se guardó. --ambiente describe el ambiente real y --lector permite otra voz con identificador anónimo. Todas estas tomas se prevén de desarrollo; no reasignan las reservas del cuento 4. Las tomas más largas y con mezcla libre requerirán revisión selectiva para establecer eventos exactos.

## Interpretación posterior

Procesar solo al cerrar el usuario la recogida completa; fijar audios/huellas/configuraciones en ese momento. Ninguna inferencia nueva durante esta preparación. Para seguimiento, comprobar la recuperación ante frases idénticas y vueltas atrás; en toma 09 el destino correcto no es el final del cuento. Para el literal, verificar intentos, sustituciones, palabras de corrección y orden real sin forzarlo al cuento. Carraspeo separado como evento no verbal; no inventar etiqueta léxica ni contarlo automáticamente como disfluencia. Mantener originales, cronología de pausas y salidas brutas. Evaluar cambios posteriores con muestras reservadas, sin adoptar resultados de estas pruebas como garantía de generalización.


## Recogida completada

26/10/2026. El lector comunica Tanda completa. Verificados doce WAV, 562,436 s (9 min 22,44 s), con huellas/cuento/cabeceras y catálogo coherentes. Referencia descriptiva y consignas previstas: datos/anotaciones/lectura_03_tanda_confirmacion.json. Sin eventos ni tiempos humanos confirmados por esa frase de finalización. Total disponible 41 audios, cuatro textos, 2.570 s con silencio; un lector. El reconocimiento queda pendiente hasta cierre explícito de toda la recogida, sin publicar ni activar cambios.
