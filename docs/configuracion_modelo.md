# Tarea 1 — Protocolo y configuración de selección

## Alcance y evaluación

- La selección de modelo, hiperparámetros y umbral se hará exclusivamente con
  la partición de desarrollo y mediante validación cruzada temporal.
- El test final queda congelado para una sola evaluación del procedimiento
  elegido. Sus resultados ya fueron reportados en la Fase 2; se declarará que
  el test ya fue observado y no se describirá como una evaluación inédita.
- El test no se usará para seleccionar o ajustar modelos, hiperparámetros ni
  umbrales.

## Modelos candidatos y validación temporal

Se evaluarán mayoría, regresión logística, SVM lineal y SVM RBF. Se usarán
particiones cronológicas comunes, sin barajar observaciones. El escalado y
cualquier otro preprocesamiento se ajustarán dentro del tramo de entrenamiento
de cada partición.

La selección se hará con particiones temporales internas. Las particiones
externas estimarán el rendimiento del procedimiento seleccionado. Para cada
partición interna y externa se reportará el número de observaciones y el número
de spikes tanto en entrenamiento como en validación. No se fijan aquí conteos
que dependen de los cortes temporales; se calcularán y mostrarán al construir
las particiones en la Tarea 2.

Se fija un mínimo de 10 spikes en cada bloque de validación usado para resumir
métricas o juzgar estabilidad, y al menos dos clases en los datos de
entrenamiento de cada partición. Si no es posible cumplirlo, se mostrarán los
conteos reales y se advertirá que las métricas de esa partición son inestables;
no se ocultará ni se compensará la falta de eventos con datos futuros.

## Umbral, scores y regla de selección

- Para logística se usarán sus probabilidades. Para ambos SVM se propone
  `CalibratedClassifierCV` con calibración sigmoide (`method="sigmoid"`) y
  particiones estrictamente cronológicas, ajustado solo dentro de cada tramo
  de entrenamiento. La calibración sigmoide se prefiere a una calibración más
  flexible porque hay pocos eventos positivos y se busca reducir el riesgo de
  sobreajuste. Se comprobará que los bloques usados para calibrar tengan ambas
  clases y se reportarán las limitaciones de calibración. Si no se pueden
  formar cortes temporales válidos, no se fingirá una probabilidad: se
  documentará el bloqueo antes de seleccionar un umbral para ese SVM.
- Para mayoría y logística se usará el score probabilístico; los SVM se calibrarán con sigmoide y cortes temporales. La grilla mixta común tiene 81 valores: 0,000–0,200 en pasos de 0,005 y 0,200–1,000 en pasos de 0,02. La mayor resolución alrededor de la prevalencia se justifica porque la calibración sigmoide puede concentrar allí las probabilidades de los SVM.
- Las probabilidades fuera de muestra para selección se generarán solo dentro
  de la validación temporal interna. La calibración, el escalado y el ajuste
  del estimador no podrán usar las etiquetas del bloque donde se evalúa cada
  score.
- Para cada modelo y umbral se reportarán recall, precisión, falsas alarmas
  (FP), falsos negativos (FN), FPR = FP / (FP + TN) y F2. La tabla completa
  mostrará además el número de observaciones y spikes evaluados.
- Un umbral cumple la tolerancia si alcanza recall ≥ 0,60 y FPR ≤ 0,50, donde
  FPR es la proporción de días regulares clasificados erróneamente como alerta.
- La estabilidad para selección se definirá como cumplir ambas condiciones en
  la mayoría estricta de las particiones internas de validación: más de la
  mitad de sus particiones válidas. Entre las configuraciones estables se
  maximizará F2 interno. Si ninguna configuración es estable, se reportará el
  mejor candidato por F2 interno sin restricción, marcado explícitamente como
  **«no cumple la tolerancia»**. La aplicación mostrará esa advertencia de
  forma visible. No se relajará la tolerancia ni se elegirá un candidato usando
  el test.
- La tabla de umbrales usada para elegir es solo una herramienta de selección;
  **no se usará como estimación de rendimiento**. El rendimiento se reportará
  con las particiones externas y, una sola vez, con el test congelado. Se
  mostrarán las métricas por partición y su resumen, incluida la frecuencia con
  que se cumple la tolerancia. Si la configuración elegida no la cumple en la
  mayoría de particiones externas, se advertirá que la tolerancia no se
  sostuvo fuera de la selección interna.
- En caso de empate de F2 interno entre configuraciones elegibles, se
  preferirá, en orden, menor variabilidad temporal de F2, modelo más sencillo
  y umbral más alto. Se reportarán los empates.

No se asignarán costos económicos a falsos positivos o falsos negativos.

## Comparación con el artículo reproducido

Se ajustará AR(11)-EGARCH(1,1)-GED en el tramo de entrenamiento y se
contrastará con AR(3)-EGARCH(2,1)-t mediante BIC, diagnósticos de residuos,
prevalencia de etiquetas y acuerdo entre etiquetas sobre fechas comunes. Como
las etiquetas y especificaciones pueden diferir, este análisis no se presentará
como comparación directa de clasificadores ni como una comparación equivalente
de desempeño predictivo.

## Interpretabilidad y errores

Para el modelo final se calculará importancia por permutación con datos de
entrenamiento y validación temporal. Se inspeccionarán casos de falsas alarmas
y spikes omitidos, indicando sus fechas y las variables disponibles. SHAP local
se probará solo en un subconjunto pequeño si resulta viable en costo e
interpretación; no será requisito para declarar el resultado.


## Referencia descriptiva trivial y tolerancia de alertas

Se reportará como referencia «alertar siempre»: recall = 1, FPR = 1 y F2 calculado en cada bloque evaluado. Esta referencia no es candidata a selección. Se excluirá de la selección cualquier umbral cuya tasa de alerta supere 95% en cualquiera de los bloques internos donde se evalúe. Si ningún candidato supera claramente la referencia trivial en F2 externo —diferencia media positiva y diferencia positiva en la mayoría estricta de particiones externas evaluables—, se escribirá explícitamente «ningún modelo mejora la referencia trivial». El mismo resultado descriptivo se reportará si el candidato elegido no cumple la tolerancia. Esta regla no es una prueba de significancia y no cambia la tolerancia recall ≥ 0,60 y FPR ≤ 0,50.

Si una partición externa no contiene bloques internos evaluables, se marca «no evaluable» y se continúa. El análisis externo se detiene solo si ninguna partición externa es evaluable. Los checkpoints incluyen hashes de las grillas, MODO_RAPIDO, cantidades de particiones internas/externas/calibración y grilla de umbrales; se guarda un checkpoint por fold interno y por partición externa. El tiempo de Colab no está medido; la celda C23T permite cronometrar un fold en modo rápido y ofrece solo una extrapolación aproximada.
