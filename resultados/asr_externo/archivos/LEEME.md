# Resultados completos de las comparativas externas

Cada TAR.GZ conserva todos los archivos originales de una cohorte: informes, configuración, selección, métricas y registros por audio/sesión. No incluye archivos de voz, pesos de modelos ni datasets de audio. Los resúmenes e informes también se mantienen sin comprimir en las carpetas de cada prueba.

`indice.json` recoge tamaños, número de archivos y SHA256 de los paquetes. Cada paquete contiene `PUBLICACION_SHA256.json` con tamaño y SHA256 de todos sus archivos; el empaquetador comprueba los miembros completos después de comprimirlos. Las referencias de texto externo conservan el contexto de procedencia de MLS en los protocolos y en `datos/externos/FUENTES.json` (Meta / Multilingual LibriSpeech, OpenSLR94, CC-BY4.0).

Para recuperar los registros detallados, ejecutar desde la raíz del proyecto, por ejemplo:

```powershell
tar -xzf resultados/asr_externo/archivos/mls_test_todos_01.tar.gz -C resultados/asr_externo
```

La extracción reconstruye `resultados/asr_externo/mls_test_todos_01`. Hacerlo sobre una copia nueva o comprobar antes que no se sobrescriben resultados propios. Los subdirectorios detallados `audios/` (JSON, no voces) y `sesiones/` quedan excluidos de Git para evitar duplicar los mismos registros comprimidos. Los archivos originales locales no se eliminan al preparar esta publicación.

Empaquetador reproducible: `scripts/empaquetar_resultados_publicables.py`. Permite reanudar comprobando los paquetes ya existentes y rechaza cualquier miembro de tipo inesperado o enlace simbólico.
