# Cuatro lecturas Android0.4 · revisión compartida

Los cuatro JSON nuevos se importaron sin modificar sus bytes; sus posiciones/movimientos se reprodujeron con el seguidor Python equivalente. Usan avance con apoyo, contexto original, dos palabras móviles y lectura_01. El usuario comunica una reducción de avances y retrocesos problemáticos. No hay audio guardado ni referencia humana por palabra para puntuar exactitud, anticipación o latencia acústica.

| Modelo | Intervalo nativo solicitado | Final | Retrocesos | PSS máximo MiB | Mayor posición estable, excluidos inicio/final |
|---|---:|---:|---:|---:|---|
| Tiny | 0,125 s | 56/56 | 0 | 243,1 | posición19:2,63 s |
| Tiny | 0,25 s | 56/56 | 1 | 233,9 | posición42:2,00 s |
| Small | 0,125 s | 56/56 | 1 | 436,9 | posición38:8,66 s |
| Small | 0,25 s | 56/56 | 0 | 450,1 | posición22:4,61 s |

Son lecturas distintas, no una comparación controlada con audio idéntico. Una posición estable puede reflejar pausa, segmentación, error ASR o rechazo del alineador; no son necesariamente segundos de retraso. En Small0,125 llegan hipótesis nuevas y varios rechazos durante la meseta: no se demuestra congelación completa de la app. Cero retrocesos tampoco prueba ausencia de avances excesivos.

La mejor sensación visual justifica seguir contrastando la variante. Se prepara como siguiente cambio independiente una guía deslizante de tres palabras, conservando modelo/cadencia/reglas. No se afirma que arregle las transcripciones ni que reduzca por sí misma la carga del reconocedor.

La cadencia adaptativa queda como propuesta separada con intervalo0,125/0,25/0,5 s, a petición del usuario: intervalo mayor al leer lento, menor al leer rápido. La falta de avance no basta para estimar ritmo lector; se deberá distinguir un atasco de una lectura pausada y registrar cambios/recursos para comparar con cadencia fija. No se ha aplicado adaptación ni se han medido sus beneficios en estas tomas.

`revision.json` contiene configuración, huellas y métricas detalladas. `limpieza_descargas.json` documenta las nueve copias verificadas antes de borrar los JSON de Lexia de Descargas, por petición del usuario. Los originales quedan en `resultados/android/sesiones/20261109`, excluidos de GitHub.
