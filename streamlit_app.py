import streamlit as st
import pandas as pd
import plotly.express as px
import random
from datetime import datetime, timedelta

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="ARCHA Cloud Dashboard",
    page_icon="🏺",
    layout="wide"
)

st.title("🏺 ARCHA Cloud – Remote Dashboard (Mock Data Preview)")

# -----------------------------
# MOCK DATA GENERATION
# -----------------------------
def generate_mock_data():
    now = datetime.now()
    timestamps = [now - timedelta(minutes=i*5) for i in range(60)][::-1]  # 60 points, 5 min apart
    temperature = [round(random.uniform(22.5, 25.5), 2) for _ in range(60)]
    humidity = [round(random.uniform(45, 65), 2) for _ in range(60)]
    pressure = [round(random.uniform(1005, 1015), 2) for _ in range(60)]
    lux = [round(random.uniform(90, 140), 2) for _ in range(60)]
    box_id = ["ATH-BOX01"] * 60

    df = pd.DataFrame({
        "timestamp": timestamps,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "lux": lux,
        "box_id": box_id
    })
    return df

df = generate_mock_data()
latest = df.iloc[-1]

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.header("📦 Rescue Box Selector")
selected_box = st.sidebar.selectbox("Active Devices:", ["ATH-BOX01", "KNS-BOX02", "DLP-BOX03"])
st.sidebar.markdown("---")
st.sidebar.write("🔋 **Battery:** 87%")
st.sidebar.write("🌐 **Wi-Fi:** Connected")
st.sidebar.write(f"🕒 **Last Sync:** {latest['timestamp'].strftime('%H:%M:%S')}")
st.sidebar.download_button("📄 Download Report", data="Example data...", file_name="archa_report.txt")

# -----------------------------
# ALERT STATUS
# -----------------------------
if latest["humidity"] > 65 or latest["temperature"] > 28:
    st.error("🔴 Critical – High humidity/temperature detected!")
elif 60 < latest["humidity"] <= 65:
    st.warning("🟡 Warning – Conditions unstable.")
else:
    st.success("🟢 Stable – Environment optimal.")

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌡️ Temp (°C)", f"{latest['temperature']:.1f}")
col2.metric("💧 Humidity (%)", f"{latest['humidity']:.1f}")
col3.metric("💡 Light (Lux)", f"{latest['lux']:.1f}")
col4.metric("📅 Time", latest['timestamp'].strftime("%H:%M"))

# -----------------------------
# GRAPHS
# -----------------------------
colA, colB = st.columns(2)

with colA:
    fig1 = px.line(df, x="timestamp", y="temperature",
                   title="🌡️ Temperature Over Time",
                   markers=True)
    fig1.update_traces(line=dict(color="orange"))
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    fig2 = px.line(df, x="timestamp", y="humidity",
                   title="💧 Humidity Over Time",
                   markers=True)
    fig2.update_traces(line=dict(color="blue"))
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# PRESSURE / LIGHT EXTRA GRAPH
# -----------------------------
colC, colD = st.columns(2)

with colC:
    fig3 = px.line(df, x="timestamp", y="pressure",
                   title="🌬️ Pressure (hPa)",
                   markers=True)
    fig3.update_traces(line=dict(color="green"))
    st.plotly_chart(fig3, use_container_width=True)

with colD:
    fig4 = px.line(df, x="timestamp", y="lux",
                   title="💡 Light Intensity (Lux)",
                   markers=True)
    fig4.update_traces(line=dict(color="gold"))
    st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Mock dashboard layout for testing | Robotic Alienz – FLL UNEARTHED 2025")
