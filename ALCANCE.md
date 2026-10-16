# Alcance inicial de lectura asistida

El objetivo final es una herramienta de lectura asistida en grupo, con turnos controlados por la profesora desde una tablet. El prototipo actual desarrolla primero el reconocimiento y seguimiento de un único lector.

## Lectura en grupo y control de la sesión

Propuesta del usuario, recogida el 16 de octubre de 2026. Pendiente de implementación; todavía no hay conexión entre la tablet de la profesora y los dispositivos del alumnado.

- La profesora selecciona al alumno que tiene el turno. Solo se habilita la captura y envío de audio de ese alumno; los demás dispositivos permanecen sin captar ni enviar audio a la sesión.
- Al cambiar de lector, se deshabilita el anterior antes de habilitar el siguiente. Cada tramo de lectura se asocia al alumno correspondiente.
- La profesora dispone de un botón **Pausar sesión** para explicaciones u otras interrupciones ajenas a la lectura. Durante la pausa no se captura ni envía audio de alumnos, no se incorpora audio al reconocimiento y se conserva la posición del cuento.
- La pausa detiene el reloj de lectura activa. Su duración se registra como interrupción docente y se excluye de las métricas del lector, sin borrar lo leído anteriormente.
- **Reanudar** devuelve el turno al mismo alumno y conserva la última posición confirmada. El nuevo tramo no se trata como audio continuo con el anterior ni se interpreta la interrupción como omisión o pausa lectora.
- Un silencio del alumno mientras la sesión está activa sigue formando parte de su lectura. No se convierte automáticamente en interrupción docente por durar cierto tiempo.

El sistema debe mostrar a la profesora si está leyendo un alumno, si la sesión está pausada o si está esperando un turno. El lector seleccionado y el estado deben coincidir con la captura efectiva de los dispositivos; perder la conexión no debe dejar un micrófono habilitado indefinidamente.

Las órdenes de pausa y cambio de turno deben impedir que audio pendiente o resultados tardíos se atribuyan a un tramo posterior. Se conservan los resultados ya confirmados y la trazabilidad de los segmentos. El tiempo total de sesión y el tiempo de lectura activa se registran por separado.

Esta decisión permite identificar las interrupciones marcadas por la profesora. No identifica retrospectivamente una interrupción que no se haya marcado. Activar un único micrófono evita recibir varios flujos a la vez, pero ese micrófono todavía puede captar voces de fondo o ruido del aula.

## Alcance del prototipo actual

- Un lector activo y un texto corto en español.
- Ordenador Windows actual; primer reconocimiento en CPU.
- Grabaciones adultas propias para depuración. No validan rendimiento infantil.
- Primera entrega: grabar, transcribir y conservar resultados y tiempos de procesamiento.
- Siguiente entrega: seguimiento incremental y subrayado de la palabra actual.
- Separar posición estimada, indicador visual y valoración de errores.
- Conservar versiones y resultados de cada prueba.
- Fuera del primer hito: cuentas, gestión de clases, control distribuido de micrófonos y pausa docente, entrenamiento y puntuación de pronunciación. La lectura grupal sigue siendo el objetivo final.

El reconocimiento inicial es posterior a la grabación. Sus tiempos por palabra son estimaciones del modelo; no son anotaciones humanas ni demuestran seguimiento en directo.

## Criterio del primer hito

Grabar el texto de datos/textos/lectura_01.txt, transcribirlo y revisar si el sistema preserva las palabras realmente pronunciadas. Repetir más adelante con una repetición, omisión y autocorrección deliberadas. No atribuir automáticamente al lector las diferencias producidas por el ASR.
