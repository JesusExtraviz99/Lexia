# Nuevos ASR · MLS dev completo

06/11/2026. El usuario comunica fin del piloto y pide comparar primero todos los nuevos con el mismo dev completo usado por los anteriores, y después reunir candidatos para test. Siete ASR nuevos, 2.408 audios dev idénticos (~10 h por motor); misma semilla, normalización, parámetros/backends y telemetría del piloto nuevo. Crisper medium/turbo/large siguen sin ejecutar. No se repite test anterior ni se incorpora un nuevo candidato sin su propia fase dev. Si ya hay test de los anteriores, conservar resultados sin repetir inferencias innecesariamente.

Antes del lote completo se comprueba el piloto 02 en el servidor: siete motores, diez audios idénticos por motor, retorno/estado correctos, firmas y archivos coherentes; bloquea límites de generación activados. Tres pruebas sintéticas del control correctas y sintaxis Bash válida. No es auditoría de métricas o escucha: recuperar también el piloto para revisar textos y recursos. Una comunicación de finalización no demuestra cero fallos.

Paquete lexia_ampliacion_dev_completo.tar, dos scripts nuevos y checksum LF. Extraer en $HOME/lexia; instala solo bajo experimentos/ampliacion_20261106. No cambia pesos, dependencias, modelos o reglas.

```bash
cd "$HOME"
sha256sum -c lexia_ampliacion_dev_completo.tar.sha256 && tar -xf lexia_ampliacion_dev_completo.tar -C "$HOME/lexia"
cd "$HOME/lexia/experimentos/ampliacion_20261106"
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_nuevos_prueba10_02
```

Con GPU libres y reservadas en calendario:

```bash
nvidia-smi
bash scripts/ejecutar_ampliacion_dev_completo.sh 0 1 2 3
```

El control inicial detiene el lanzamiento si el piloto presenta problemas; no saltárselo ni borrar su evidencia. Para un piloto con otro número, usar LEXIA_PILOTO_COHORTE=mls_dev_nuevos_prueba10_N explícito.

Envoltorio nohup, stdin /dev/null y salida+errores a .lanzador.log. Continúa tras cerrar SSH/VPN/PC en condiciones normales; un reinicio/cancelación del servidor puede interrumpirlo. PID guardado no acredita arranque correcto: verificar log/progreso. Una tarea propia por GPU autorizada, restantes en cola; sin fallback CPU. Rechaza resultados/log/PID previos.

```bash
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_nuevos_completo_01
tail -n 20 resultados/asr_externo/mls_dev_nuevos_completo_01.lanzador.log
```

Al finalizar, cada uno de los siete debe completar 2408/2408 y cero fallos. Se compararán mismos audios y métricas, dejando explícitas diferencias de backend, capacidad y concurrencia. Tiempos no equivalen a coste aislado ni rendimiento móvil. No se afirma aún resultado o ejecución remota.
