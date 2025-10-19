import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="ARCHA Cloud Dashboard", page_icon="🏺", layout="wide")
st.title("🏺 ARCHA Cloud – Remote Dashboard")

FIREBASE_URL = "https://archa-cloud-default-rtdb.firebaseio.com/readings.json"

@st.cache_data(ttl=30)
def get_data():
    r = requests.get(FIREBASE_URL)
    data = r.json()
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data.values())
    df = df.sort_values("timestamp")
    return df

df = get_data()
if df.empty:
    st.warning("Waiting for data from Rescue Boxes…")
    st.stop()

latest = df.iloc[-1]
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temp (°C)", f"{latest['temperature']:.1f}")
col2.metric("💧 Humidity (%)", f"{latest['humidity']:.1f}")
col3.metric("💡 Lux", f"{latest['lux']:.1f}")
col4.metric("📦 Box", latest['box_id'])

if latest['humidity'] > 65 or latest['temperature'] > 28:
    st.error("🔴 Critical – High humidity/temperature!")
elif 60 < latest['humidity'] <= 65:
    st.warning("🟡 Warning – Conditions unstable.")
else:
    st.success("🟢 Stable – Environment optimal.")

colA, colB = st.columns(2)
with colA:
    fig1 = px.line(df, x="timestamp", y="temperature", title="🌡️ Temperature Over Time")
    st.plotly_chart(fig1, use_container_width=True)
with colB:
    fig2 = px.line(df, x="timestamp", y="humidity", title="💧 Humidity Over Time")
    st.plotly_chart(fig2, use_container_width=True)

st.caption("Data source: Firebase Realtime DB | Robotic Alienz – FLL UNEARTHED")
