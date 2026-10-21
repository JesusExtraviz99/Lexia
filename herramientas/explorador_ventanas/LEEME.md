# Explorador acústico de ventanas

Herramienta local de consulta para escuchar qué fragmento recibe el ASR en cada corte guardado, comparar ventanas y consultar las decisiones de los tres seguidores. No graba, no modifica anotaciones ni ejecuta inferencias.

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\python.exe -u -m scripts.explorar_ventanas resultados/comparaciones/20261021_090720_432047 --puerto 8771
```

Abrir http://127.0.0.1:8771/ y mantener el proceso activo. Ctrl+C lo cierra.

Elegir ronda y corte; escuchar cada ventana con los botones o controles de audio. Velocidades 1/0,8/0,6/0,4 y repetición opcional. El audio se remuestrea a mono 16 kHz mediante el mismo decodificador del experimento; cada clip se recorta por muestras y se entrega como WAV PCM16. La cuantización de reproducción no es una inferencia nueva. Muestra el fragmento de entrada, no los recortes internos del VAD. El texto ASR permanece fijo al cambiar la velocidad.

Las posiciones experimentales se reproducen con el código actual; se verifica que el original coincida con el registro. El candidato global mostrado es diagnóstico, no significa que el original lo haya ejecutado/aceptado en ese corte. Los tiempos de salida reutilizan la cola simulada original y no añaden coste de variantes ni pantalla.

Comprobaciones de creación: seis originales reproducidos, 180 límites de audio validados; ocho clips de cortes 32/34/36/38 de ventanas 4/8 comprobados muestra a muestra dentro del error PCM16. JavaScript sin errores de sintaxis. En navegador se comprobaron cambio de corte y reproducción de clips de 4 y 8 segundos, sin errores de audio y con reproducción excluyente.
