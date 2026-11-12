# Proyecto Integrador ML2: alertas de eventos extremos de la TRM

Entrega integrada de las Fases 1, 2 y 3: un notebook ejecutable, resultados curados, una app Streamlit de reproducción histórica y el informe final en LaTeX/PDF.

## Estado de la corrida de referencia

La corrida completa disponible es `20261112T220020597329Z`, ejecutada localmente en Windows con Python 3.13.17 y las versiones registradas en `results/final/registro_versiones.csv`.

- GARCH: AR(3)-EGARCH(2,1)-t, BIC 9792.143375; convergieron 94 de 108 especificaciones.
- Selección de desarrollo: regresión logística, C=10, umbral 0.44. El candidato **no cumple la tolerancia** recall >= 0.60 y FPR <= 0.50.
- Comparación externa: ningún candidato mejora descriptivamente la referencia «alertar siempre» en F2.
- Test congelado: 684 observaciones, 33 spikes; evaluación registrada una vez, luego de la selección. La regresión logística obtuvo recall 0.969697 y 639 falsas alarmas. El test ya se había reportado en Fase 2 y no se usó para seleccionar.
- El archivo de metadatos de C29 registra `status=completed`, `usado_para_seleccion=false` y el SHA-256 del modelo.

Los valores del informe se basan en esta corrida y sustituyen las cifras anteriores cuando difieren. La corrida está verificada en el entorno local; la rama de arranque y ejecución en Colab todavía no se ha validado.

## Archivos principales

- `Proyecto_ML2_Final.ipynb`: notebook único de las tres fases.
- `data/`: CSV de TRM y tasa BanRep; snapshots fijados por el manifiesto.
- `results/final/`: tablas y metadatos curados de la corrida de referencia.
- `results/runs/`: checkpoints y salidas completas locales; excluidos de Git.
- `figures/informe_final/`: figuras actualizadas usadas por el informe.
- `app/app.py`: app Streamlit sin descargas ni predicción en vivo.
- `docs/guion_sustentacion_fase3.md`: guion alineado con los resultados.
- `informe/informe_final_fase3.tex` y `informe_final_fase3.pdf`: fuente y PDF integrados.
- `requirements.txt`: dependencias fijadas para el entorno local.
- `requirements-colab.txt`: pins de dependencias directas para Colab.

## Reproducir en local

Desde `entrega/`, instala las versiones fijadas:

```powershell
python -m pip install -r requirements.txt
```

Abre el notebook desde esta carpeta o establece `ML2_PROJECT_DIR` apuntando a `entrega/`. Ejecuta las celdas en orden. Las fuentes primarias son los CSV y snapshots locales; las consultas en línea son verificaciones opcionales. Si falta un archivo requerido, el notebook se detiene en vez de inventar o interpolar datos.

Para iniciar la app después de ejecutar C27 (que prepara el artefacto y el archivo local de reproducción):

```powershell
python -m streamlit run app/app.py
```

La app arrancó en el `.venv` local y el endpoint de salud de Streamlit respondió `ok`. La app muestra score, umbral, alerta y las advertencias de tolerancia. Reproduce fechas históricas locales; no es una predicción en vivo.

## Google Colab

La primera celda de arranque espera una URL HTTPS y un SHA completo de GitHub. **Aún no existe URL ni commit publicados.** En un checkout público, el notebook solicita subir los snapshots de mercado y EMBI si no están presentes; C02 valida los ocho archivos fijados. No se reinstalan numpy, pandas ni scikit-learn; C03 registra las versiones efectivas y advierte sobre diferencias.

## política de datos y publicación

Los snapshots Yahoo Finance y EMBI están excluidos por `.gitignore` hasta confirmar sus condiciones de redistribución. El README no autoriza su publicación. Para que la app pueda reproducirse desde un clon, se requiere ejecutar primero el notebook con todos los datos autorizados. No hay repositorio remoto de GitHub publicado todavía; faltan la decisión de snapshots y la creación/fijación del commit.

## Informe

Abre `informe/informe_final_fase3.tex` en TeXstudio y compila con XeLaTeX. El cuerpo del informe cumple tres páginas narrativas, excluyendo portada, bibliografía, tablas y figuras. Las tablas y figuras se numeran y se interpretan en el texto. El PDF final está en `informe/informe_final_fase3.pdf`.
