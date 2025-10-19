import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# --------------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------------
st.set_page_config(page_title="ARCHA Cloud Dashboard", page_icon="🏺", layout="wide")

# --------------------------------------------------------
# CUSTOM RESPONSIVE CSS + COLORED PANELS
# --------------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f9f9fb;
    font-family: "Helvetica Neue", sans-serif;
}

/* Header bar */
.title-bar {
    background-color: #1e5ab6;
    color: white;
    padding: 0.8rem 1.5rem;
    border-radius: 0 0 10px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}
.title-left {
    font-weight: 600;
    font-size: 1.4rem;
}
.nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
    font-size: 1rem;
}

/* Card container */
.card {
    background: white;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}

/* Metric colored panels */
.metric-row {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}
.metric-box {
    border-radius: 12px;
    color: white;
    text-align: center;
    padding: 1rem 1rem;
    width: 100%;
    font-weight: bold;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.15);
}
.temp-box { background: linear-gradient(180deg, #f39c12 0%, #e67e22 100%); }
.humid-box { background: linear-gradient(180deg, #c0392b 0%, #a93226 100%); }
.light-box { background: linear-gradient(180deg, #3498db 0%, #2980b9 100%); }

.metric-value {
    font-size: 1.8rem;
    margin-bottom: 0.2rem;
}
.metric-label {
    font-size: 0.9rem;
    opacity: 0.9;
}

/* Responsive layout for small screens */
@media (max-width: 768px) {
    .block-container { padding: 0.5rem !important; }
    .title-bar { flex-direction: column; align-items: flex-start; }
    .metric-value { font-size: 1.4rem; }
    .nav a { display: none; }
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# HEADER BAR
# --------------------------------------------------------
st.markdown("""
<div class="title-bar">
    <div class="title-left">☁️ ARCHA Cloud</div>
    <div class="nav">
        <a href="#">Dashboard</a>
        <a href="#">Sites</a>
        <a href="#">Artifacts</a>
        <a href="#">Alerts</a>
        <a href="#">🔍</a>
        <a href="#">👤</a>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# MOCK SENSOR DATA
# --------------------------------------------------------
now = datetime.now()
timestamps = [now - timedelta(hours=i) for i in range(24)][::-1]
temperature = [round(random.uniform(19, 25), 1) for _ in range(24)]
humidity = [round(random.uniform(50, 80), 1) for _ in range(24)]
light = [round(random.uniform(100, 240), 1) for _ in range(24)]
df = pd.DataFrame({"Time": timestamps, "Temperature": temperature,
                   "Humidity": humidity, "Light": light})
latest = df.iloc[-1]

# --------------------------------------------------------
# LAYOUT
# --------------------------------------------------------
col1, col2, col3 = st.columns([1.2, 1.6, 1.2])

# LEFT COLUMN – RESCUE BOX INFO + COLORED PANELS
with col1:
    st.markdown(f"""
    <div class="card">
        <h4>RESCUE BOX 2</h4>
        <p><b>Artifact ID:</b> K126-01<br>
           <b>Material:</b> Wood<br>
           <b>Site:</b> Poseidi</p>
        <div class="metric-row">
            <div class="metric-box temp-box">
                <div class="metric-value">{latest['Temperature']}°C</div>
                <div class="metric-label">Temperature</div>
            </div>
            <div class="metric-box humid-box">
                <div class="metric-value">{latest['Humidity']}%</div>
                <div class="metric-label">Relative Humidity</div>
            </div>
            <div class="metric-box light-box">
                <div class="metric-value">{latest['Light']} lux</div>
                <div class="metric-label">Light Level</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# MIDDLE COLUMN – CHART
with col2:
    st.markdown('<div class="card"><h4>ENVIRONMENTAL DATA</h4>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Temperature"], name="Temperature", line=dict(color="#e67e22")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Humidity"], name="Rel. Humidity", line=dict(color="#c0392b")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Light"], name="Light", line=dict(color="#2980b9")))
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=20, b=10),
                      xaxis_title="", yaxis_title="Value", template="plotly_white",
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN – MAP
with col3:
    st.markdown('<div class="card"><h4>ARTIFACT CONDITION: WOOD</h4>', unsafe_allow_html=True)
    m = folium.Map(location=[39.9, 23.4], zoom_start=6)
    folium.Marker([39.9, 23.4], tooltip="Poseidi").add_to(m)
    st_folium(m, height=200, width=None)
    st.markdown('<button style="background:#1e5ab6;color:white;padding:6px 14px;border:none;border-radius:6px;margin-top:6px;">View Details</button>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------------
# SECOND ROW – AI RECOMMENDATIONS & ALERTS
# --------------------------------------------------------
col4, col5, col6 = st.columns([1.2, 1.6, 1.2])

with col4:
    st.markdown("""
    <div class="card">
        <h4>AI PRESERVATION RECOMMENDATION</h4>
        <p style="color:#e74c3c;font-weight:bold;">⚠️ High humidity detected<br>Add desiccant</p>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="card">
        <h4>AI PRESERVATION ANALYSIS</h4>
        <p>Elevated humidity can cause swelling, warping, or mold growth.</p>
    </div>
    """, unsafe_allow_html=True)
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=["45%", "55%", "60%", "80%"], y=[1, 3, 4, 3], marker_color="#3498db"))
    bar_fig.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10),
                          xaxis_title="", yaxis_title="Risk Level", template="plotly_white")
    st.plotly_chart(bar_fig, use_container_width=True)

with col6:
    st.markdown("""
    <div class="card">
        <h4>RECENT ALERTS</h4>
        <p><b>Poseidi</b><br>Jan. 18 2024 02:15<br>
        <span style="color:#e74c3c;font-weight:bold;">⚠️ High humidity</span></p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------------
# FOOTER
# --------------------------------------------------------
st.markdown("<br><center><small>ARCHA Cloud © 2025 – Robotic Alienz | FLL UNEARTHED</small></center>", unsafe_allow_html=True)
