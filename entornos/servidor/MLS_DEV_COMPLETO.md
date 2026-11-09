# MLS dev completo · cinco reconocedores

Preparado el 04/11/2026 tras autorización del usuario y auditoría de la prueba de diez audios. Se procesan los 2.408 archivos oficiales dev (35.959,18 s, aproximadamente diez horas por motor), una vez por motor. Test permanece reservado. Mismos pesos, revisiones, entradas mono/16 kHz, decodificadores, float32 cuando procede y semilla que en el piloto; sin introducir VAD, limpieza o cambios de reconocimiento.

## Actualización y diferencias frente al piloto

El coordinador requiere --limite 0 --completo explícitos para admitir dev completo. Mantiene una tarea por GPU autorizada y Vosk CPU. La generación de Markdown/CSV/resumen se hace cada 50 audios y al finalizar; se mantienen resúmenes ligeros en memoria, evitando releer todos los JSON anteriores tras cada audio. Los JSON originales por audio, progreso.json y las muestras JSONL se guardan durante la ejecución. Estas diferencias de E/S/código quedan registradas; no tratar el piloto como réplica idéntica de rendimiento.

La reanudación individual --reanudar requiere la misma firma/configuración/GPU/archivos. Omite audios correctos y errores definitivos ya guardados. Un audio interrumpido por KeyboardInterrupt puede repetirse y conserva antes el intento previo en intentos/. El coordinador no reanuda automáticamente una cohorte antigua: ante un fallo revisaremos los estados antes de decidir el comando de recuperación. No sobrescribir carpetas ni borrar resultados para repetir.

El lanzador se ejecuta con nohup, stdin cerrado y log redirigido: puede continuar después de cerrar SSH en condiciones normales. Un reinicio del servidor, falta de recursos o una cancelación administrativa pueden terminarlo. Verificar el progreso después del inicio; imprimir un PID no demuestra que la evaluación esté funcionando. Se conservan logs y salidas parciales.

## Transferir la actualización

PowerShell local:

```powershell
cd 'C:\Users\PC\OneDrive\Documentos\ChatGPT\Practicas y TFG'
scp '.\.descartados\servidor\lexia_mls_dev_completo.tar' '.\.descartados\servidor\lexia_mls_dev_completo.tar.sha256' jextraviz@192.168.22.24:/opt/qaisc/home/jextraviz/
```

SSH:

```bash
cd "$HOME"
sha256sum -c lexia_mls_dev_completo.tar.sha256 && tar -xf lexia_mls_dev_completo.tar -C "$HOME/lexia"
cd "$HOME/lexia"
nvidia-smi
```

El paquete incluye evaluador, adaptadores, coordinador, consulta de progreso, envoltorio nohup y este documento. No incluye datos, modelos ni dependencias; no necesita reinstalarlos. Los pesos y resultados del piloto se conservan. No reextraer después los paquetes anteriores, porque contienen versiones previas del evaluador/coordinador.

## Iniciar

Indicar únicamente GPU que os hayan permitido usar. Con las cuatro 0–3:

```bash
cd "$HOME/lexia"
bash scripts/ejecutar_mls_dev_completo.sh 0 1 2 3
```

Los candidatos GPU se distribuyen entre las plazas explícitas disponibles; los restantes esperan. Si se utiliza una lista menor, el resto se encola. Vosk usa CPU. No se reservan tarjetas de forma atómica frente a otros usuarios: la asignación debe coordinarse con la empresa. El envoltorio rechaza salida/log/PID existentes, evitando lanzar por accidente otra copia con el mismo nombre.

Salidas: resultados/asr_externo/mls_dev_completo_paralela_01. Log general: el mismo nombre con sufijo .lanzador.log; PID: .pid. Todos los audios/transcripciones de prueba anteriores permanecen en su carpeta.

## Comprobar avance

```bash
cd "$HOME/lexia"
python3 scripts/estado_asr_externo.py resultados/asr_externo/mls_dev_completo_paralela_01
tail -n 20 resultados/asr_externo/mls_dev_completo_paralela_01.lanzador.log
```

Durante preflight/carga puede aparecer «preparando» o loading. Cada modelo debe llegar a 2408/2408, fallos=0 y completed. El coordinador tarda hasta su siguiente consulta en reflejar las finalizaciones. Para detalles de un motor:

```bash
tail -n 15 resultados/asr_externo/mls_dev_completo_paralela_01/crisper.log
```

Cambiar crisper por xlsr, parakeet, whisper o vosk. Consultar estos archivos no ejecuta ASR. La fecha de última actualización es UTC. No reiniciar el envoltorio si ya está trabajando.

## Medición y comprobaciones posteriores

Se conserva toda la instrumentación del piloto y sus límites: muestras CPU/RAM del proceso y estado global, memoria privada/compartida disponible, E/S, GPU física/PID, potencia/temperatura/frecuencias y detalle de límites del driver, versiones y huellas; carga/calentamiento separados. Los máximos muestreados y energía cubierta no equivalen a picos garantizados o consumo neto por audio. Los intervalos rápidos pueden seguir sin muestras GPU individuales; evaluar coste sostenido y allocator Torch por separado.

No deducir ausencia de errores porque un proceso devuelva 0. Al terminar, recuperar los informes y comprobar cobertura exacta de los 2.408 IDs, mismos hashes/referencias entre motores, estados, WER/CER recalculados, avisos, límites de generación y telemetría. CPU/GPU concurrentes comparten recursos; se medirán después selecciones aisladas para comparar rendimiento. Mantener las referencias originales y no corregirlas selectivamente después de ver hipótesis.

Fuentes exactas de los scripts del piloto se conservan localmente en su carpeta fuentes_ejecucion antes de esta actualización. Validación de la actualización: 16 pruebas locales, con FLAC/motores/procesos simulados; incluyen lote completo de un dataset sintético, informes periódicos, progreso y recuperación de interrupción conservando el intento anterior. Sintaxis Bash/Python comprobada. No se ha ejecutado aún MLS completo desde esta máquina ni se declara iniciado hasta recibir evidencia del servidor.
