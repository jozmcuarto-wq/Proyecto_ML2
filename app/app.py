from pathlib import Path
import hashlib,json,joblib,numpy as np,pandas as pd,streamlit as st
D=Path(__file__).resolve().parent; M=D/"model.joblib"; X=D/"data"/"reproduccion_historica.csv"
st.set_page_config(page_title="TRM histórica")
st.title("Reproducción histórica de alertas de TRM")
st.warning("Reproduce scores históricos locales; no es predicción en vivo.")
if not M.is_file() or not X.is_file(): st.error("Ejecuta C24 y C27 en el notebook."); st.stop()
b=joblib.load(M); meta=json.loads((D/"app_metadata.json").read_text(encoding="utf-8"))
if hashlib.sha256(M.read_bytes()).hexdigest()!=meta["model_sha256"]: st.error("Hash del modelo no coincide."); st.stop()
df=pd.read_csv(X,parse_dates=["fecha"]); features=b["features"]
st.caption(f'{b["modelo"]} | umbral={b["umbral"]:.5f} | run_id={b["run_id"]}')
if not b["cumple_tolerancia"]: st.error("El modelo NO cumple la tolerancia predefinida.")
if not b.get("alguno_mejora_referencia_trivial",False): st.warning("Ningún modelo mejora claramente alertar siempre en F2 externo.")
day=st.selectbox("Fecha historica",df.fecha.dt.strftime("%Y-%m-%d"))
row=df.loc[df.fecha.dt.strftime("%Y-%m-%d").eq(day),features].iloc[[0]]
est=b["estimador"]
if isinstance(est,dict) and {"base","calibrator"}.issubset(est):
    z=np.asarray(est["base"].decision_function(row)).reshape(-1,1); score=float(est["calibrator"].predict_proba(z)[0,1])
else: score=float(est.predict_proba(row)[0,1])
st.metric("Score",f"{score:.4f}"); st.metric("Umbral",f'{b["umbral"]:.4f}')
st.success("ALERTA" if score>=b["umbral"] else "Sin alerta")
