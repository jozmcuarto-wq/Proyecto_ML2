# Proyecto Integrador ML2: detección de spikes de la TRM

Proyecto de series de tiempo y aprendizaje automático para estudiar y detectar movimientos extremos de la tasa representativa del mercado (TRM) de Colombia. El proyecto cubre la construcción de etiquetas, el análisis de predictores financieros y la evaluación temporal de modelos de clasificación.

## Qué hace el proyecto

- **Fase 1:** reconstruye y limpia la serie de TRM, calcula retornos, estima modelos GARCH y construye etiquetas de spikes. Incluye diagnósticos de series de tiempo y una línea base de clasificación.
- **Fase 2:** añade predictores de mercado, EMBI y tasa de intervención. Alinea las series por fecha y evalúa modelos con particiones cronológicas.
- **Fase 3:** compara modelos mediante validación temporal, selecciona un umbral usando F2 y reporta el compromiso entre detección y falsas alarmas. Incluye una comparación con la especificación del artículo, análisis de importancia por permutación y una aplicación de reproducción histórica.

Los resultados muestran una señal predictiva débil y falsas alarmas frecuentes. La aplicación reproduce datos históricos; **no es un sistema de predicción en vivo**.

## Contenido del repositorio

- `Proyecto_ML2_Final.ipynb`: notebook único con el flujo de las tres fases.
- `data/`: datos de entrada y snapshots utilizados para reconstruir la corrida.
- `docs/`: configuración del protocolo y guion de sustentación.
- `figures/`: figuras incluidas en el informe.
- `app/app.py`: aplicación Streamlit.
- `informe_final_fase3.pdf`: informe integrado.
- `requirements.txt`: versiones de referencia local.
- `requirements-colab.txt`: versiones de referencia para Colab.
- `.gitignore`: excluye entornos virtuales, cachés y resultados temporales.

**No se subió la carpeta `results/`.** El notebook genera los resultados de cada ejecución en la ruta indicada por `RUN_DIR`. Los CSV de referencia de Fase 2 tampoco están publicados; si faltan, la celda de comparación lo advierte y continúa sin esa comparación.

## Datos y reproducibilidad

El notebook usa los archivos de `data/` y sus snapshots como entradas primarias. No sustituye silenciosamente un snapshot faltante por una descarga nueva ni inventa o interpola datos. Valida los archivos requeridos y registra la procedencia de las fuentes.

Por condiciones de redistribución, algunos snapshots de mercado pueden no estar incluidos en el repositorio. Si el notebook los solicita, proporciona los archivos indicados por la celda de carga. La descarga opcional de fuentes sirve para verificar datos; no reemplaza los snapshots fijados.

## Ejecutar en Google Colab

1. Abre el notebook: [Proyecto_ML2_Final.ipynb en Colab](https://colab.research.google.com/github/jozmcuarto-wq/Proyecto_ML2/blob/main/Proyecto_ML2_Final.ipynb).
2. Ejecuta las celdas en orden. La celda de inicio solicita la URL del repositorio y el SHA completo del commit para fijar la versión del código.
3. Si se solicitan snapshots que no están en el repositorio, carga los archivos indicados con sus nombres originales.
4. Ejecuta el notebook de principio a fin. Las celdas guardan los resultados en la carpeta de ejecución que informa `RUN_DIR`.

Si la validación del entorno indica que falta `arch`, ejecuta antes de C03:

```python
%pip install --no-deps "arch==9.0.0"
