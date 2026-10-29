# Intentos parciales: ablaciones del literal

Exploración de desarrollo sobre tomas 2/3; 5/6 reservadas intactas. Mismo prefijo VAD para cada ablación, un solo parámetro distinto. Referencia original reutilizada, no benchmark pareado. El recorte del último bloque cambia entrada y contexto: contraste separado, no aislación causal de un parámetro. Marcas automáticas no son tiempos humanos. No se suministra cuento, palabra objetivo o transcripción como prompt. Sin cambios del seguidor.


## toma_3 · audio 0.00–70.32 s

**Referencia reutilizada:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**sin_reparacion** (16.74 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**sin_temperaturas_alternativas** (17.10 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.

**sin_recuperacion_cierre** (17.39 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una pe- pe- pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara abrió el papel y leyó:"Busca donde termina el sendero". Los dos siguieron despacio hasta un viejo molino. Allí des des descubrieron una puerta escondida entre las plantas. Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.


## toma_2 · audio 0.00–65.84 s

**Referencia reutilizada:** Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto.

**sin_reparacion** (17.20 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto.

**sin_temperaturas_alternativas** (17.40 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto.

**sin_recuperacion_cierre** (17.17 s): Una mañana Mateo salió a caminar con su hermana Clara. Junto al puente encontraron una una pequeña caja de madera. Dentro había una llave, una pluma azul y un papel doblado. Clara Clara abrió el papel y leyó, busca donde termina el sendero. Los dos siguieron despacio hasta un viejo molino, allí descubrieron una puerta escondida entre las plantas. Mateo Mateo probó la llave, pero no consiguió abrirla. Entonces Clara levantó una piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto junto al puente para que alguien más pudiera descubrir el secreto.


## toma_3_ultimo_bloque · audio 52.00–70.32 s

**recorte_ajustes_originales** (5.46 s): Piedra y encontró otra entrada. Detrás había un jardín lleno de flores. Antes de regresar, dejaron la caja junto al puente para que alguien más pudiera descubrir el secreto.


Las salidas no se corrigen ni convierten automáticamente en eventos. El objetivo humano confirmado es regres- re- regresar; no se entrega al modelo. Recorte a partir de 52 s según bloque automático, no límite humano de palabra. Las variantes pueden no ejecutar internamente una ruta desactivada: igualdad de salida no prueba que esa ruta causase o no el error. CPU/RAM/GPU global en resultados.json; inferencia excluye carga y VAD previo. Sin rendimiento móvil ni precisión global.
