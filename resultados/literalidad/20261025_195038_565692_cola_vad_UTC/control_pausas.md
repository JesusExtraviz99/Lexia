# Control de pausas largas dentro de la lectura

25/10/2026. Los casos originales 3 y 13 no estaban en la primera tanda de ocho entradas con límite VAD. Se ensayan ahora con el mismo tratamiento y parámetros, en una carpeta nueva.

- Audio 3, pausa flor–Ana: las marcas del lector delimitan flor hasta 11,88 s y Ana desde 21,20 s, separación de 9,32 s. Ese intervalo queda dentro del prefijo enviado y es idéntico muestra a muestra al original; se conservan las tres anclas disponibles, incluida cuaderno al final. El texto hablado escrito es el mismo que antes; solo desaparece la etiqueta final automática [throatclearing], cuya corrección no se ha adjudicado por escucha nueva. Persiste la omisión previa de a en llamó a su hermano.
- Audio 13, pausa con relectura de Junto a una fuente…: se conservan el prefijo completo y la pausa interior comunicada como unos 8 s, sin duración humana precisa. La salida nueva es idéntica a la anterior y mantiene dos apariciones textuales de la frase repetida. Eso no garantiza que todo el resto sea correcto: siguen formas previas como de espacio y para acercar a la orilla.

Los originales de 60 y 50 s pasan a entradas de 31,376 y 41,776 s. El límite se obtiene de la última voz detectada en el archivo completo, no del primer silencio; no se unen fragmentos eliminando pausas. Esto verifica análisis offline, no la política de parada/reanudación de una sesión en directo.

Inferencia previa reutilizada: 38,98 s; nueva: 21,21 s; carga nueva: 7,91 s. Recursos y versiones completos en candidato.json/metricas.json; VAD reutilizado del diagnóstico anterior. Una pasada, procesos de diferente tamaño y estado del equipo, sin extrapolar a tablet. Pasan 85 pruebas antes de inferir. Integridad, tres anclas e intervalo manual verificados, sin cambios de los WAV previos.

Visor http://127.0.0.1:8779/: conserva la numeración original 3/13; permite escuchar original completo o prefijo enviado y comparar ambos textos. Pendiente de revisión compartida. La variante sigue experimental y no se publica automáticamente.
