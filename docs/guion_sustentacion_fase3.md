# Guion de sustentación — Proyecto Integrador ML2

## 1. Problema y artículo

Nuestro objetivo es detectar si el retorno diario de la TRM USD/COP presenta un spike. La etiqueta se construye con la regla $|\hat\varepsilon_t|>2\hat\sigma_t$ del modelo econométrico. El artículo de referencia propone GARCH-SVM para Bitcoin; adaptamos esa idea a la TRM, conservando la generación GARCH de etiquetas y el contraste con SVM. La adaptación no es una reproducción idéntica del activo o de la muestra.

## 2. Datos y validación

La TRM viene de Datos Abiertos Colombia, la tasa de intervención de la serie oficial BanRep, EMBI de BCRPData y las variables de mercado de snapshots fijados con hash. La TRM cruda y válida tiene 8.364 filas; quedan 8.363 retornos, 8.360 etiquetas GARCH y 8.354 observaciones de clasificación. El panel de Fase 2 tiene 6.835 observaciones y 338 spikes.

Los retornos de mercado y EMBI se alinean hacia atrás con tolerancia de cinco días; BanRep, sin tolerancia, porque la tasa permanece vigente hasta el siguiente cambio. Los predictores se alinean antes de la validación y solo usan datos de la fecha de origen o anteriores. Imputación y escalado se ajustan en los folds. La validación es cronológica y anidada. El test ya se había reportado en Fase 2, no se usó para seleccionar, y C29 lo evaluó una única vez tras congelar la configuración.

## 3. Modelo GARCH y Fases 1 y 2

De 108 especificaciones convergieron 94. La ganadora fue AR(3)-EGARCH(2,1)-t, con BIC 9792.143375. El ADF rechaza raíz unitaria en retornos; KPSS reporta p=0.10 como límite de la tabla. Ljung-Box detecta autocorrelación en residuos estandarizados; los residuos cuadrados y ARCH-LM no muestran heterocedasticidad residual.

En Fase 1, la mayoría logra 94.86% de exactitud pero no identifica spikes. La logística balanceada obtiene 46.51% de recall y 6.27% de precisión. En Fase 2, con 33 spikes en test, logística y SVM lineal detectan 30, pero producen 548 y 595 falsas alarmas; RBF detecta 22 y produce 344. El AP más alto es 0.098710 frente a una prevalencia de 0.048246. Es una señal débil, no una capacidad de alerta confiable.

## 4. Selección de Fase 3 y resultado externo

El protocolo maximiza F2 en validación interna y exige de forma estable recall >= 0.60 y FPR <= 0.50. La configuración seleccionada fue logística con C=10 y umbral 0.44, pero queda declarada «no cumple la tolerancia». No se relajó el requisito. Ningún candidato superó claramente en F2 externo la regla «alertar siempre».

La logística tuvo F2 externo medio 0.204322 (DE 0.017645), recall 0.861388 y FPR 0.860327. La alta tasa de alerta implica numerosas falsas alarmas. No se hicieron pruebas de significancia entre modelos.

## 5. Comparación con el artículo e interpretación

En la muestra común de 7.515 fechas con hold_back=11, el artículo AR(11)-EGARCH(1,1)-GED tiene BIC 9891.252739 y la adaptación AR(3)-EGARCH(2,1)-t 9771.697991; las etiquetas concuerdan en 99.32%. Es comparación econométrica in-sample, no una comparación entre clasificadores, y esos BIC no se comparan con el BIC de la búsqueda C09.

La permutación se calculó solo en las validaciones externas. El retorno rezagado de TRM mostró la mayor caída media de AP (0.001744), con magnitudes pequeñas e inestables. Predictores correlacionados pueden repartirse importancia; no interpretamos la permutación como causalidad. SHAP se dejó desactivado. En los bloques externos hubo 4.018 falsas alarmas y 33 spikes omitidos.

## 6. Test congelado y demostración

C29 evaluó una vez las 684 observaciones de test, con 33 spikes. Para logística con C=10 y umbral 0.44, la matriz es [[12,639],[1,32]], recall 96.97%, precisión 4.77%, F2 0.199253 y AP 0.080308. Hubo 639 falsas alarmas. Este resultado no se usó para volver a elegir el modelo; el test ya se conocía por Fase 2, así que no representa una muestra independiente recién descubierta.

Para la demostración local, ejecutar primero C27 y después `python -m streamlit run app/app.py`. Seleccionar una fecha histórica; la app muestra score, umbral, decisión y advertencias. Aclarar que es reproducción local, sin descargas y sin predicción en vivo. Mostrar explícitamente que el modelo no cumple la tolerancia y que ningún modelo supera claramente «alertar siempre».

## 7. Limitaciones y cierre

Hay alta falta de cobertura en Brent, MXN y CLP; la etiqueta depende del modelo GARCH; persiste autocorrelación en residuos; solo hay cuatro particiones externas y 33 eventos en test. La precisión es baja, las falsas alarmas son numerosas y no existen pruebas de significancia ni costos económicos estimados. La conclusión es un flujo reproducible y una app demostrativa, no un sistema listo para generar alertas operativas.

## Declaración de uso de IA generativa

Claude se usó para redactar prompts, interpretar reportes, diagnosticar errores de entorno y sugerir redacción. Codex se usó para la auditoría y edición técnica del notebook y del informe. La corrida del notebook la hizo la persona estudiante.
