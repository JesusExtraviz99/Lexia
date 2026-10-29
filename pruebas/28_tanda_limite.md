# Tanda de mayor dificultad: La caja del sendero

26/10/2026. Preparación de seis grabaciones adicionales del mismo cuento para explorar límites del seguimiento y del análisis literal. No sustituye la tanda anterior ni sus controles. Las consignas están en datos/textos/lectura_04_tomas_limite.json y el texto original en lectura_04.txt. Son dificultades simuladas por un adulto; no datos clínicos ni evaluación final independiente.

## Grabación

```powershell
.\.venv\Scripts\python.exe -u -m scripts.grabar_tanda --plan datos/textos/lectura_04_tomas_limite.json
```

Enter inicia cada toma y un segundo Enter la termina y guarda. Muestra consigna y cuento, reutiliza el grabador y asigna nombres reales Limite 1–6, con fecha y cuento, en datos/audio. Antes de la siguiente toma vuelve a esperar Enter. No se inicia ningún ASR. Los tiempos indicados son límites máximos, 1.020 s (17 minutos) si se agotan todos; se puede terminar antes sin esperar. Se guarda la duración real capturada, sin añadir silencio hasta el máximo. Puedes dejar un breve margen después de la última palabra antes de pulsar Enter para conservar su final. No usar Ctrl+C para guardar antes. Si una toma no se termina, comunicarlo en vez de darla por completa.

| Toma | Máximo | Fenómeno previsto |
|---|---:|---|
| 1 | 150 s | Tres cadenas de intentos parciales: pequeña, descubrieron y regresar. |
| 2 | 150 s | Roja→azul, ventana→puerta y Clara→Mateo, con correcciones explícitas. |
| 3 | 180 s | Retroceso de tres frases y continuación hasta el final. |
| 4 | 180 s | Una frase omitida inicialmente, pronunciada después fuera de orden. |
| 5 | 180 s | Pausa dentro de pequeña, pausa entre frases y ritmos lento/rápido/habitual. |
| 6 | 180 s | Mezcla exploratoria libre. |

Tiempos de pausas aproximados por consigna, no medición humana. Los fenómenos de 5/6 se combinan deliberadamente; no permiten atribuir un fallo a una sola causa. Todas estas nuevas tomas se destinan a exploración de desarrollo; no cambian la reserva de tomas 5/6 de la tanda anterior.

Para consultar sin grabar, añadir --listar. Para reanudar, usar el mismo --plan y --desde N. --ambiente permite describir condiciones reales; --lector distingue nuevas voces con identificadores anónimos. Mantener micrófono/distancia y evitar ruido deliberado primero; ruido real no se presupone ausente. No cambiar --cuento sin adaptar las consignas: aquí contienen palabras concretas de lectura_04.

## Recogida y reconocimiento posterior

El usuario quiere grabar primero estas seis tomas y después otros cuentos. No ejecutar reconocimiento automáticamente al aparecer nuevos WAV: esperar a que indique que ha terminado de reunir el lote. Entonces congelar una selección explícita de identificadores y huellas, comprobar qué audios ya tienen resultados y procesar únicamente los nuevos con configuración fija. Procesar el lote secuencialmente, conservando resultados y recursos por grabación; comparar entornos después sobre los mismos audios. Repetir inferencia no aumenta el número de grabaciones.

La referencia para estadísticas es lo que se oye, no el cuento ni la consigna. Mantener salida literal bruta, fenómenos confirmados, eventos dudosos y tiempos humanos por separado. Para el seguimiento interesa posición/recuperación; para el literal, intentos conservados, omisiones e inserciones. Alcanzar el final no valida ambas tareas. Conservar controles fluidos y registrar condiciones/texto/lector además de dificultad. No es necesario transcribir a mano todos los silencios: priorizar eventos que sustentan cada métrica.

## Estado al preparar

Catálogo verificado: 23 WAV propios disponibles, 1.550 s (25 min 50 s de archivo, con silencios), tres textos grabados y un adulto. Las seis nuevas tomas todavía no están grabadas. No se ejecutan inferencias ni se publica este estado automáticamente.


## Recogida completada

26/10/2026. Seis WAV verificados, duraciones 69,654 / 70,710 / 61,772 / 49,562 / 85,728 / 120,143 s; total 457,568 s. El lector comunica finalización de la tanda. En toma 6 añade estornudo deliberado cerca del final y una lectura Clara abrió el papel y leyó: Busca donde empieza el sendero seguida de la frase entera correcta; otras trabadas sin detalle. El estornudo se separa como evento vocal no verbal y no se cuenta automáticamente como disfluencia. Sin tiempos humanos ni transcripción exhaustiva. Referencia descriptiva con huellas en datos/anotaciones/lectura_04_limite_confirmacion.json. ASR pendiente hasta cierre de la recogida por el usuario.
