# Ruta de trabajo de Lexia

Actualización: 19/10/2026. Estado de desarrollo, no porcentaje de finalización del TFG. El alcance de aula y selección de lector por el docente está en ALCANCE.md.

| Bloque | Estado | Resultado o criterio para avanzar |
|---|---|---|
| 1. Prototipo técnico | Completado para pruebas locales | Grabación, transcripción, alineamiento con cuento y simulación de seguimiento con ventanas. |
| 2. Primera evaluación adulta | Completada con alcance limitado | Lectura normal, desviaciones deliberadas, pausa, lectura lenta y relectura. Referencia temporal completa del caso normal y selectiva de tres eventos. Se conocen fallos y coste de cómputo; no es validación general. |
| 3. Mejorar el seguidor | Siguiente bloque | Revisar evidencia escasa en habla lenta, recuperación y retrocesos. Comparar cada cambio con los mismos registros y mantener la versión anterior como referencia. |
| 4. Comparar reconocimiento y ejecución | Pendiente | Comparar una selección de modelos/configuraciones con los mismos audios, referencias y métricas. Separar cambio de modelo, hardware y periodo de actualización. Medir posición, transcripción, coste, cola y estabilidad. |
| 5. Comparar ayudas de audio | Pendiente | Variar VAD y reducción de ruido por separado y después sus combinaciones en las opciones finalistas. El sistema actual ya usa VAD: aún no se ha hecho una comparación controlada con VAD desactivado. |
| 6. Prototipo funcional en directo | Pendiente | Micrófono y seguimiento visible con medición real de demora; interfaz y control del docente conforme al alcance. Las herramientas actuales de anotación no son la aplicación de aula. |
| 7. Validación en otros casos y entornos | Pendiente | Reservar voces, cuentos y sesiones no usados para ajustar parámetros; comparar condiciones acústicas y micrófonos. Evaluar con el mismo protocolo y con ayudas activadas/desactivadas en una selección viable. Validación infantil y uso profesional requieren sus propios datos y evaluación. |
| 8. Consolidación del TFG | En curso y cierre pendiente | Diario, protocolos, registros y versiones se mantienen desde el inicio. Al final: síntesis de resultados, límites, decisiones y demostración reproducible. |

Los bloques pueden solaparse cuando haya una razón documentada. No se debe seguir ajustando sobre datos reservados y presentarlos después como validación independiente.

## Experimento inmediato propuesto

Pregunta: ¿puede el seguidor avanzar en lectura lenta cuando solo hay una palabra fiable disponible, sin introducir avances o retrocesos erróneos en los demás casos?

1. Conservar el seguidor actual como comparación inicial.
2. Reproducir primero las hipótesis ASR ya guardadas, conservando ventanas, cortes y orden. Esto aísla el cambio del seguidor y evita repetir reconocimiento para cada variante.
3. Probar una regla acotada de aceptación de evidencia escasa. No aceptar cualquier palabra aislada: estudiar coincidencia con el cuento y contexto de seguimiento. La regla definitiva queda pendiente de implementación y comprobación.
4. Contrastar lectura normal, desviaciones, pausa, lenta y relectura. Medir recuperación después de Después, llegada y estabilidad del final, movimientos durante pausas y comportamiento ante repetición real.
5. Comparar el coste propio del seguidor. Si se reutilizan tiempos de inferencia anteriores, identificarlos como reutilizados: no presentarlos como nuevas medidas completas de rendimiento de la variante.
6. Conservar o descartar el cambio según resultados. Después estudiar posiciones provisionales/respaldadas, retrocesos y política de actualización en experimentos separados.

No se necesitan nuevas grabaciones ni más marcas para comenzar este experimento. Los casos actuales son datos de desarrollo: mejorar en ellos no demuestra generalización.

## Cómo comparar entornos sin multiplicar pruebas sin límite

Para software y ayudas, reutilizar exactamente los mismos WAV cuando sea posible. Para otra sala, micrófono o persona hacen falta nuevas grabaciones con un protocolo comparable; no son señales idénticas. Seleccionar primero configuraciones prometedoras y después contrastarlas en otros entornos, conservando condiciones con y sin ayudas. Comparar todo con todo desde el principio aumenta trabajo y dificulta atribuir las diferencias.

## Situación actual

La hipótesis puede estar cerca de la referencia en lectura normal mientras la salida visible simulada llega tarde. La pausa conserva la posición en los cortes observados. La lectura lenta pierde el final o retrocede después de alcanzarlo. La frase repetida aparece en el texto ASR, pero no se demuestra seguimiento temporal completo de la relectura. Aún no hay medición de latencia real de pantalla ni elección definitiva de modelo, ventana o combinación de ayudas.

Detalle de evidencias y límites: pruebas/10_revision_eventos.md y docs/DIARIO_DESARROLLO.md.
