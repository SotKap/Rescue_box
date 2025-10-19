import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import random

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(page_title="ARCHA Cloud Dashboard", page_icon="🏺", layout="wide")

# --------------------------
# CUSTOM CSS STYLING
# --------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f9f9fb;
        padding: 0;
    }
    .title-bar {
        background-color: #1e5ab6;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 0 0 10px 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .title-left {
        font-weight: 600;
        font-size: 1.4rem;
    }
    .nav {
        font-size: 1rem;
    }
    .nav a {
        color: white;
        text-decoration: none;
        margin: 0 10px;
    }
    .card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .label {
        color: #555;
        font-size: 0.9rem;
    }
    .warning {
        color: #e74c3c;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# HEADER BAR
# --------------------------
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

# --------------------------
# MOCK DATA
# --------------------------
now = datetime.now()
timestamps = [now - timedelta(hours=i) for i in range(24)][::-1]
temperature = [round(random.uniform(19, 25), 1) for _ in range(24)]
humidity = [round(random.uniform(50, 80), 1) for _ in range(24)]
light = [round(random.uniform(100, 240), 1) for _ in range(24)]
df = pd.DataFrame({"Time": timestamps, "Temperature": temperature,
                   "Humidity": humidity, "Light": light})

# --------------------------
# LAYOUT
# --------------------------
col1, col2, col3 = st.columns([1.2, 1.6, 1.2])

# LEFT CARD – RESCUE BOX INFO
with col1:
    st.markdown("""
    <div class="card">
        <h4>RESCUE BOX 2</h4>
        <p><b>Artifact ID:</b> K126-01<br>
           <b>Material:</b> Wood<br>
           <b>Site:</b> Poseidi</p>
        <div style="background:#f9f9f9;border-radius:8px;padding:8px;margin-top:10px;">
            <div class="metric" style="color:#e67e22;">20.3°C</div>
            <div class="label">Temperature</div>
        </div>
        <div style="background:#f9f9f9;border-radius:8px;padding:8px;margin-top:10px;">
            <div class="metric" style="color:#c0392b;">78%</div>
            <div class="label">Relative Humidity</div>
        </div>
        <div style="background:#f9f9f9;border-radius:8px;padding:8px;margin-top:10px;">
            <div class="metric" style="color:#2980b9;">220 lux</div>
            <div class="label">Light Level</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# MIDDLE CARD – ENVIRONMENTAL DATA CHART
with col2:
    st.markdown('<div class="card"><h4>ENVIRONMENTAL DATA</h4>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Temperature"], name="Temperature", line=dict(color="#e67e22")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Humidity"], name="Rel. Humidity", line=dict(color="#6c5ce7")))
    fig.add_trace(go.Scatter(x=df["Time"], y=df["Light"], name="Light", line=dict(color="#3498db")))
    fig.update_layout(height=260, margin=dict(l=10, r=10, t=20, b=10),
                      xaxis_title="", yaxis_title="%",
                      template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT CARD – MAP
with col3:
    st.markdown('<div class="card"><h4>ARTIFACT CONDITION: WOOD</h4>', unsafe_allow_html=True)
    m = folium.Map(location=[39.9, 23.4], zoom_start=6)
    folium.Marker([39.9, 23.4], tooltip="Poseidi").add_to(m)
    st_folium(m, height=220, width=300)
    st.markdown('<a href="#" style="text-decoration:none;"><button style="background:#1e5ab6;color:white;padding:6px 14px;border:none;border-radius:6px;margin-top:6px;">View Details</button></a>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# SECOND ROW
col4, col5, col6 = st.columns([1.2, 1.6, 1.2])

# LEFT CARD – AI RECOMMENDATION
with col4:
    st.markdown("""
    <div class="card">
        <h4>AI PRESERVATION RECOMMENDATION</h4>
        <p class="warning">⚠️ High humidity detected<br>Add desiccant</p>
    </div>
    """, unsafe_allow_html=True)

# MIDDLE CARD – MATERIAL WARNING GRAPH
with col5:
    st.markdown("""
    <div class="card">
        <h4>AI PRESERVATION ANALYSIS</h4>
        <p>Elevated humidity can cause swelling, warping, or mold growth.</p>
    </div>
    """, unsafe_allow_html=True)
    # Simple bar chart
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=["45%", "55%", "60%", "80%"], y=[1, 3, 4, 3], marker_color="#3498db"))
    bar_fig.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10),
                          xaxis_title="", yaxis_title="Risk Level", template="plotly_white")
    st.plotly_chart(bar_fig, use_container_width=True)

# RIGHT CARD – ALERTS
with col6:
    st.markdown("""
    <div class="card">
        <h4>RECENT ALERTS</h4>
        <p><b>Poseidi</b><br>Jan. 18 2024 02:15<br>
        <span class="warning">⚠️ High humidity</span></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><center><small>ARCHA Cloud Dashboard – Mock Layout | Robotic Alienz FLL UNEARTHED</small></center>", unsafe_allow_html=True)
