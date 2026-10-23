# Tercer texto: una frase con dos apariciones

Preparación: 23/10/2026. Texto original datos/textos/lectura_03.txt. Objetivo: ampliar el banco con una ambigüedad textual natural. La frase «El tren llegó a la estación» aparece dos veces. Esto no es una disfluencia del lector: ambas apariciones forman parte del texto esperado.

Versión inicial: 77 palabras; frase en posiciones 1–6 y 41–46; final casa (77). SHA256 del texto: df744c7d5747ef235be121ae875e50b5bbea7484d2b85b99c40cd6d5da67d6f6.

Primero grabar un control: cuento completo una sola vez, ritmo natural, sin comentarios y silencio al terminar. Duración disponible 60 s. La grabadora espera Enter del usuario. Registrar el ambiente que realmente haya; no dar por hecho que sigue lloviendo. Guardar el WAV crudo. No cambiar modelo, reglas ni filtros.

```powershell
.\.venv\Scripts\python.exe scripts\grabar.py --segundos 60 --cuento .\datos\textos\lectura_03.txt --nombre "Lectura normal - cuento 3 - frase repetida" --caso normal --lector adulto_01
```

Después de recibir la ruta y confirmar el contenido, comparar ventanas 4/8 s, tres rondas de cómputo. Pasar explícitamente --cuento .\datos\textos\lectura_03.txt. Comprobar la trayectoria en ambas apariciones, destino final y retrocesos, además de métricas de tiempo y recursos. No limitarse a la posición final. Comparar las tres variantes con las mismas hipótesis mediante comparar_relectura_lejana --control-sin-relectura.

Después del control se podrá grabar una vuelta desde el final a la frase repetida. Una frase idéntica por sí sola no identifica cuál de las dos apariciones pretende releer la persona. Documentar la intención en la consigna y contrastar con el audio; no contar automáticamente ausencia de recuperación global exacta como fallo: la regla exige una aparición única. El contexto circundante y la búsqueda local pueden producir otras decisiones. No anticipar que ventanas o variantes deban dar el mismo resultado.

Es una prueba de desarrollo con el mismo adulto, no un test reservado ni validación de lectura infantil. No hay audio, anclas ni resultados nuevos todavía. No activar variantes ni publicar automáticamente.
