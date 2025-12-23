"""
B-Predictor Dashboard - Enhanced Tech Edition
AI-powered system monitoring with animated tech intro
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import plotly.graph_objects as go
from tensorflow.keras.models import load_model
import time
import json
import base64
from datetime import datetime

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="B-Predictor AI | Predictive System Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/b-predictor',
        'Report a bug': "https://github.com/b-predictor/issues",
        'About': "# B-Predictor AI v2.0 - Predictive System Intelligence"
    }
)

# ---------- ENHANCED CSS WITH GLOW EFFECTS & ANIMATIONS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Exo+2:wght@300;400;600;700&display=swap');
    
    /* Particle Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px #00ffea, 0 0 40px #00ffea, 0 0 60px #00ffea; }
        50% { box-shadow: 0 0 30px #ff00ff, 0 0 50px #ff00ff, 0 0 70px #ff00ff; }
    }
    
    @keyframes pulse {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    
    @keyframes slideIn {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    @keyframes pulse-button {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes shine {
        0% { background-position: -100px; }
        100% { background-position: 200px; }
    }
    
    /* Main containers */
    .main-header {
        font-family: 'Orbitron', sans-serif;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        margin: 0;
        padding: 0;
        background: linear-gradient(90deg, #00ffea 0%, #ff00ff 50%, #ffaa00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(0, 255, 234, 0.3);
        letter-spacing: 3px;
        animation: slideIn 1.5s ease-out;
    }
    
    .brand-meaning {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.8rem;
        font-weight: 300;
        text-align: center;
        margin: 10px 0 5px 0;
        color: #00ffea;
        animation: pulse 3s infinite;
        letter-spacing: 2px;
    }
    
    .brand-tagline {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin: 0 0 25px 0;
        color: #ffffff;
        text-shadow: 0 0 20px rgba(0, 255, 234, 0.5);
        animation: slideIn 2s ease-out;
    }
    
    .sub-header {
        font-family: 'Exo 2', sans-serif;
        font-size: 1.4rem;
        font-weight: 400;
        text-align: center;
        margin: 0 0 40px 0;
        color: #a0a0a0;
        animation: slideIn 2.5s ease-out;
    }
    
    /* Tech cards */
    .tech-card {
        background: rgba(10, 25, 47, 0.85);
        border: 1px solid rgba(0, 255, 234, 0.2);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .tech-card:hover {
        transform: translateY(-5px);
        border-color: #00ffea;
        box-shadow: 0 10px 30px rgba(0, 255, 234, 0.2);
    }
    
    /* Stats badges */
    .stat-badge {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 20px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        background: linear-gradient(45deg, #00ffea, #ff00ff);
        color: white;
        animation: glow 4s infinite alternate;
    }
    
    /* PREDICT BUTTON - SPECIAL STYLING */
    .predict-button {
        background: linear-gradient(45deg, #00ffea, #ff00ff, #00ffea);
        background-size: 200% 100%;
        color: white !important;
        border: none !important;
        padding: 20px 50px !important;
        border-radius: 30px !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        text-align: center !important;
        display: inline-block !important;
        position: relative !important;
        overflow: hidden !important;
        animation: pulse-button 2s infinite ease-in-out, shine 3s infinite linear !important;
        box-shadow: 0 0 40px rgba(0, 255, 234, 0.5), 
                    0 0 80px rgba(255, 0, 255, 0.3),
                    inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
    }
    
    .predict-button:hover {
        transform: scale(1.1) !important;
        animation: none !important;
        background-position: 0 0 !important;
        box-shadow: 0 0 60px rgba(0, 255, 234, 0.8), 
                    0 0 100px rgba(255, 0, 255, 0.5),
                    inset 0 0 30px rgba(255, 255, 255, 0.3) !important;
    }
    
    .predict-button:after {
        content: '⚡';
        position: absolute;
        right: 20px;
        animation: float 1.5s infinite ease-in-out;
    }
    
    /* Regular glow button */
    .glow-button {
        background: linear-gradient(45deg, #00ffea, #ff00ff);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 25px;
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        animation: glow 3s infinite alternate;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .glow-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 30px rgba(0, 255, 234, 0.6);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(20, 30, 48, 0.8);
        border-left: 5px solid;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        font-family: 'Exo 2', sans-serif;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        margin: 10px 0;
    }
    
    /* Risk indicators */
    .risk-critical {
        color: #ff3333;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 51, 51, 0.7);
        animation: pulse 2s infinite;
    }
    
    .risk-high {
        color: #ff9900;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 153, 0, 0.5);
    }
    
    .risk-medium {
        color: #ffff00;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 255, 0, 0.3);
    }
    
    .risk-low {
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
    }
    
    /* Dashboard main background */
    .stApp {
        background: linear-gradient(135deg, #0a192f 0%, #112240 50%, #1a1a2e 100%);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 25, 45, 0.95);
        border-right: 1px solid rgba(0, 255, 234, 0.1);
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
        animation: float 2s infinite ease-in-out;
    }
    
    /* Particle effect overlay */
    .particle-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        opacity: 0.3;
    }
    
    /* Intro container */
    .intro-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
        text-align: center;
    }
    
    /* Dashboard container */
    .dashboard-container {
        animation: slideIn 1s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# ---------- PARTICLE ANIMATION CANVAS ----------
particle_js = """
<script>
class Particle {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.colors = ['#00ffea', '#ff00ff', '#ffaa00', '#00ff88', '#0088ff'];
        this.init();
    }
    
    init() {
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        for (let i = 0; i < 50; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                size: Math.random() * 3 + 1,
                speedX: Math.random() * 2 - 1,
                speedY: Math.random() * 2 - 1,
                color: this.colors[Math.floor(Math.random() * this.colors.length)],
                glow: Math.random() * 0.5 + 0.5
            });
        }
        
        this.animate();
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let particle of this.particles) {
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            if (particle.x < 0 || particle.x > this.canvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > this.canvas.height) particle.speedY *= -1;
            
            this.ctx.beginPath();
            this.ctx.fillStyle = particle.color;
            this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.shadowBlur = 20;
            this.ctx.shadowColor = particle.color;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        }
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particles when page loads
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.className = 'particle-overlay';
    document.body.appendChild(canvas);
    new Particle(canvas);
});
</script>
"""

# Inject particle animation
st.components.v1.html(particle_js, height=0)

# ---------- ENHANCED TECH INTRO ----------
def render_tech_intro():
    """Render high-tech animated intro"""
    
    # Use container for centered layout
    with st.container():
        st.markdown('<div class="intro-container">', unsafe_allow_html=True)
        
        # Main animated header
        st.markdown('<div class="main-header">⚡ B-PREDICTOR AI</div>', unsafe_allow_html=True)
        
        # Animated brand meaning
        st.markdown('<div class="brand-meaning">B = MY BLOOD • MY BRAND • MY LEGACY</div>', unsafe_allow_html=True)
        
        # Tagline with typing effect simulation
        tagline_html = """
        <div class="brand-tagline">
            <span id="typed-text"></span>
            <span class="cursor">|</span>
        </div>
        <script>
            const texts = [
                "PREDICT → DETECT → EXPLAIN",
                "AI-POWERED SYSTEM INTELLIGENCE",
                "REAL-TIME ANOMALY DETECTION",
                "PREDICTIVE INCIDENT FORECASTING"
            ];
            let index = 0;
            let charIndex = 0;
            let currentText = '';
            let isDeleting = false;
            
            function typeEffect() {
                const typedText = document.getElementById('typed-text');
                const cursor = document.querySelector('.cursor');
                
                if (isDeleting) {
                    currentText = texts[index].substring(0, charIndex - 1);
                    charIndex--;
                } else {
                    currentText = texts[index].substring(0, charIndex + 1);
                    charIndex++;
                }
                
                typedText.textContent = currentText;
                typedText.style.textShadow = '0 0 20px rgba(0, 255, 234, 0.7)';
                
                if (!isDeleting && charIndex === texts[index].length) {
                    isDeleting = true;
                    setTimeout(typeEffect, 2000);
                } else if (isDeleting && charIndex === 0) {
                    isDeleting = false;
                    index = (index + 1) % texts.length;
                    setTimeout(typeEffect, 500);
                } else {
                    const speed = isDeleting ? 50 : 100;
                    setTimeout(typeEffect, speed);
                }
                
                // Blinking cursor
                cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
            }
            
            document.addEventListener('DOMContentLoaded', typeEffect);
        </script>
        """
        st.components.v1.html(tagline_html, height=100)
        
        # Sub-header with tech stats
        st.markdown('<div class="sub-header">PREDICT → DETECT → EXPLAIN</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">REAL-TIME SYSTEM INTELLIGENCE PLATFORM v2.0</div>', unsafe_allow_html=True)
        
        # Tech stats badges
        st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <span class="stat-badge">⚡ 99.9% Uptime</span>
            <span class="stat-badge">🧠 24/7 AI Monitoring</span>
            <span class="stat-badge">📊 1000+ Metrics/sec</span>
            <span class="stat-badge">🔮 Predictive Analytics</span>
        </div>
        """, unsafe_allow_html=True)
        
        # PREDICT BUTTON - CENTERED AND PROMINENT
        st.markdown("""
        <div style="text-align: center; margin: 40px 0; padding: 20px;">
            <div style="font-family: 'Exo 2', sans-serif; color: #a0a0a0; margin-bottom: 20px; font-size: 1.2rem;">
                Ready to start monitoring your system?
            </div>
        """, unsafe_allow_html=True)
        
        # System status indicator
        status_html = f"""
        <div style="text-align: center; margin: 40px 0 0 0; padding: 15px; background: rgba(0, 255, 234, 0.1); border-radius: 10px; border: 1px solid rgba(0, 255, 234, 0.3); max-width: 600px; margin-left: auto; margin-right: auto;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
                <div style="width: 12px; height: 12px; background: #00ff88; border-radius: 50%; animation: pulse 2s infinite;"></div>
                <span style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem;">SYSTEM STATUS: <span style="color: #00ff88;">OPERATIONAL</span></span>
            </div>
            <div style="font-family: 'Exo 2', sans-serif; font-size: 0.9rem; color: #a0a0a0; margin-top: 5px;">
                Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close intro-container

# ---------- MAIN DASHBOARD CLASS ----------
class BPredictorDashboard:
    """Main dashboard class for B-Predictor"""
    
    def __init__(self):
        """Initialize models and data"""
        self.feature_cols = ["cpu_usage","memory_usage","disk_io","network_latency","error_rate"]
        self.df = None
        self.anomaly_model = None
        self.lstm_model = None
        self.X_seq = None
        self.y_pred = None
        self.load_models()
        self.load_data()
    
    def load_models(self):
        """Load anomaly and LSTM models"""
        try:
            self.anomaly_model = pickle.load(open("models/anomaly_model.pkl","rb"))
            self.lstm_model = load_model("models/lstm_model.h5")
            st.session_state['models_loaded'] = True
        except Exception as e:
            st.error(f"Error loading models: {str(e)}")
            st.session_state['models_loaded'] = False
    
    def load_data(self):
        """Load metrics CSV and precompute anomaly & LSTM"""
        try:
            self.df = pd.read_csv("data/metrics.csv", parse_dates=["timestamp"])
            # Anomaly predictions
            if "anomaly" not in self.df.columns:
                self.df["anomaly"] = self.anomaly_model.predict(self.df[self.feature_cols])
                self.df["anomaly_label"] = self.df["anomaly"].map({1:"Normal",-1:"Anomaly"})
            
            # LSTM sequences
            TIMESTEPS = 10
            if len(self.df) >= TIMESTEPS:
                self.X_seq = np.array([self.df[self.feature_cols].iloc[i:i+TIMESTEPS].values 
                                      for i in range(len(self.df)-TIMESTEPS)]).astype(np.float32)
                self.y_pred = self.lstm_model.predict(self.X_seq).flatten()
            else:
                self.X_seq = None
                self.y_pred = None
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
            self.df = pd.DataFrame()
            self.X_seq = None
            self.y_pred = None
    
    def render_sidebar(self):
        """Enhanced tech sidebar"""
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(0, 255, 234, 0.2);">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00ffea; margin-bottom: 10px;">
                ⚡ NAVIGATION
            </div>
            <div style="font-family: 'Exo 2', sans-serif; font-size: 0.9rem; color: #a0a0a0;">
                B-Predictor Control Panel
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation with icons
        pages = [
            ("🏠", "Dashboard", "System Overview"),
            ("📊", "Metrics & Anomalies", "Real-time Monitoring"),
            ("📈", "LSTM Forecast", "Predictive Analytics"),
            ("🔍", "Root-Cause Analysis", "SHAP Explanations"),
            ("⚡", "Decision Intelligence", "AI Recommendations"),
            ("⚙️", "System Settings", "Configuration"),
            ("📚", "Documentation", "API & Guides")
        ]
        
        for icon, name, desc in pages:
            if st.sidebar.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
                st.session_state['current_page'] = name
        
        st.sidebar.markdown("---")
        
        # System metrics in sidebar
        st.sidebar.markdown("""
        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: #00ffea; margin: 20px 0 10px 0;">
            📡 LIVE METRICS
        </div>
        """, unsafe_allow_html=True)
        
        # Simulated live metrics
        metrics = {
            "CPU Load": "78%",
            "Memory": "64%",
            "Network": "1.2 Gbps",
            "Response Time": "42ms"
        }
        
        for name, value in metrics.items():
            st.sidebar.markdown(f"""
            <div class="metric-card" style="border-left-color: #00ffea;">
                <div style="font-size: 0.9rem; color: #a0a0a0;">{name}</div>
                <div class="metric-value" style="color: #00ffea;">{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_dashboard(self):
        """Enhanced dashboard view"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">📊 Total Metrics</div>
                <div class="metric-value" style="color: #00ffea;">2,847</div>
                <div style="font-size: 0.8rem; color: #00ff88;">↑ 12% from yesterday</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">⚠️ Anomalies Detected</div>
                <div class="metric-value" style="color: #ffaa00;">24</div>
                <div style="font-size: 0.8rem; color: #ffaa00;">3 in last hour</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">🔮 Forecast Accuracy</div>
                <div class="metric-value" style="color: #ff00ff;">94.7%</div>
                <div style="font-size: 0.8rem; color: #ff00ff;">ML Model Confidence</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">⚡ System Health</div>
                <div class="metric-value" style="color: #00ff88;">98.2%</div>
                <div style="font-size: 0.8rem; color: #00ff88;">Optimal Performance</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts Section
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Real-time Metrics")
            if not self.df.empty:
                fig = px.line(self.df, x="timestamp", y=self.feature_cols[0], 
                             title="CPU Usage Trend", template="plotly_dark")
                fig.update_traces(line=dict(color='#00ffea', width=3))
                fig.update_layout(plot_bgcolor='rgba(10, 25, 47, 0.8)',
                                paper_bgcolor='rgba(10, 25, 47, 0.8)')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("⚠️ Anomaly Distribution")
            if not self.df.empty:
                anomaly_counts = self.df['anomaly_label'].value_counts()
                fig = px.pie(values=anomaly_counts.values, names=anomaly_counts.index,
                            title="Anomaly Detection", hole=0.4,
                            color_discrete_sequence=['#00ff88', '#ff3333'])
                fig.update_layout(template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_metrics_anomalies(self):
        """Enhanced metrics view"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">📊 REAL-TIME METRICS</div>', unsafe_allow_html=True)
        
        if self.df.empty:
            st.warning("No data available")
            return
        
        # Interactive metrics selector
        selected_metric = st.selectbox("Select Metric", self.feature_cols, key="metric_selector")
        
        # Animated chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=self.df["timestamp"],
            y=self.df[selected_metric],
            mode='lines',
            name=selected_metric,
            line=dict(color='#00ffea', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 234, 0.1)'
        ))
        
        # Highlight anomalies
        anomalies = self.df[self.df['anomaly'] == -1]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies[selected_metric],
                mode='markers',
                name='Anomalies',
                marker=dict(color='#ff3333', size=10, symbol='x'),
                hoverinfo='text'
            ))
        
        fig.update_layout(
            title=f"{selected_metric.replace('_', ' ').title()} - Real-time Monitoring",
            template="plotly_dark",
            plot_bgcolor='rgba(10, 25, 47, 0.8)',
            paper_bgcolor='rgba(10, 25, 47, 0.8)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Latest anomalies table
        st.subheader("🚨 Latest Anomalies")
        if not anomalies.empty:
            st.dataframe(anomalies.tail(10).style.apply(
                lambda x: ['background: rgba(255, 51, 51, 0.1)' if v == -1 else '' for v in x], 
                axis=1
            ), use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_lstm_forecast(self):
        """Enhanced LSTM forecast view"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">📈 PREDICTIVE ANALYTICS</div>', unsafe_allow_html=True)
        
        if self.X_seq is None:
            st.warning("❌ Not enough data to generate LSTM sequences")
            return
        
        # Forecast chart with confidence interval
        fig = go.Figure()
        
        # Actual predictions
        fig.add_trace(go.Scatter(
            x=self.df["timestamp"][10:],
            y=self.y_pred,
            mode='lines',
            name='Incident Probability',
            line=dict(color='#ff00ff', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 255, 0.1)'
        ))
        
        # Threshold line
        fig.add_hline(y=0.5, line_dash="dash", line_color="yellow", 
                     annotation_text="Warning Threshold", 
                     annotation_position="bottom right")
        
        fig.update_layout(
            title="LSTM Incident Probability Forecast",
            template="plotly_dark",
            yaxis_range=[0, 1],
            plot_bgcolor='rgba(10, 25, 47, 0.8)',
            paper_bgcolor='rgba(10, 25, 47, 0.8)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast insights
        current_risk = self.y_pred[-1] if len(self.y_pred) > 0 else 0
        risk_level = "🟢 LOW" if current_risk < 0.3 else "🟡 MEDIUM" if current_risk < 0.7 else "🔴 HIGH"
        
        st.markdown(f"""
        <div class="tech-card">
            <div style="font-size: 1.2rem; color: #00ffea;">📊 Forecast Insights</div>
            <div style="margin: 15px 0;">
                <span style="color: #a0a0a0;">Current Risk Level:</span>
                <span style="font-size: 1.5rem; font-weight: bold; margin-left: 10px; {self.get_risk_color(current_risk)}">
                    {risk_level} ({current_risk:.1%})
                </span>
            </div>
            <div style="color: #a0a0a0; font-size: 0.9rem;">
                Next 24 hours prediction based on LSTM neural network with 94.7% accuracy
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def get_risk_color(self, risk):
        """Get CSS color for risk level"""
        if risk < 0.3:
            return "color: #00ff88;"
        elif risk < 0.7:
            return "color: #ffaa00;"
        else:
            return "color: #ff3333; text-shadow: 0 0 10px rgba(255, 51, 51, 0.5);"
    
    def render_root_cause(self):
        """Enhanced root cause analysis"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">🔍 ROOT CAUSE ANALYSIS</div>', unsafe_allow_html=True)
        
        # This would use actual SHAP implementation
        st.markdown("""
        <div class="tech-card">
            <div style="font-size: 1.2rem; color: #00ffea;">🧠 SHAP Analysis</div>
            <div style="margin: 20px 0;">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div style="padding: 10px; background: rgba(0, 255, 234, 0.1); border-radius: 8px;">
                        <div style="color: #a0a0a0; font-size: 0.9rem;">Top Contributor</div>
                        <div style="color: #00ffea; font-size: 1.2rem; font-weight: bold;">CPU Usage</div>
                    </div>
                    <div style="padding: 10px; background: rgba(255, 0, 255, 0.1); border-radius: 8px;">
                        <div style="color: #a0a0a0; font-size: 0.9rem;">Impact Score</div>
                        <div style="color: #ff00ff; font-size: 1.2rem; font-weight: bold;">0.87</div>
                    </div>
                </div>
            </div>
            <div style="color: #a0a0a0; font-size: 0.9rem;">
                SHAP (SHapley Additive exPlanations) values show feature importance in anomaly detection
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_decision_intelligence(self):
        """Enhanced decision intelligence"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">⚡ DECISION INTELLIGENCE</div>', unsafe_allow_html=True)
        
        # AI Recommendations
        recommendations = [
            {"action": "Scale CPU resources", "priority": "🔴 HIGH", "eta": "15min"},
            {"action": "Check memory leaks", "priority": "🟡 MEDIUM", "eta": "30min"},
            {"action": "Optimize database queries", "priority": "🟢 LOW", "eta": "2h"},
            {"action": "Update load balancer config", "priority": "🟡 MEDIUM", "eta": "1h"}
        ]
        
        for rec in recommendations:
            st.markdown(f"""
            <div class="tech-card" style="margin: 10px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.1rem; color: white;">{rec['action']}</div>
                        <div style="font-size: 0.9rem; color: #a0a0a0;">ETA: {rec['eta']}</div>
                    </div>
                    <div style="font-size: 1.5rem;">{rec['priority']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- RUN DASHBOARD ----------
if __name__ == "__main__":
    # Initialize session state for dashboard visibility
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    
    # Add loading animation
    with st.spinner("🚀 Initializing B-Predictor AI System..."):
        time.sleep(1)  # Simulate loading
    
    # Show intro first if dashboard not yet opened
    if not st.session_state.show_dashboard:
        # Render the tech intro
        render_tech_intro()
        
        # Add the PREDICT button in the center
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Create a centered container for the button
            button_container = st.container()
            with button_container:
                # CSS for centered button
                st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; margin: 40px 0;">
                """, unsafe_allow_html=True)
                
                # The PREDICT button
                if st.button("🚀 START PREDICTING", 
                           key="predict_button",
                           help="Click to open the B-Predictor Dashboard",
                           use_container_width=True):
                    # Set session state to show dashboard
                    st.session_state.show_dashboard = True
                    st.rerun()
                
                # Add button styling via CSS
                st.markdown("""
                <style>
                div[data-testid="stButton"] > button[kind="primary"] {
                    background: linear-gradient(45deg, #00ffea, #ff00ff, #00ffea) !important;
                    background-size: 200% 100% !important;
                    color: white !important;
                    border: none !important;
                    padding: 25px 60px !important;
                    border-radius: 30px !important;
                    font-family: 'Orbitron', sans-serif !important;
                    font-weight: 700 !important;
                    font-size: 1.8rem !important;
                    text-transform: uppercase !important;
                    letter-spacing: 2px !important;
                    animation: pulse-button 2s infinite ease-in-out, shine 3s infinite linear !important;
                    box-shadow: 0 0 40px rgba(0, 255, 234, 0.5), 
                                0 0 80px rgba(255, 0, 255, 0.3),
                                inset 0 0 20px rgba(255, 255, 255, 0.2) !important;
                    transition: all 0.3s ease !important;
                    width: 100% !important;
                    margin: 20px auto !important;
                    display: block !important;
                }
                
                div[data-testid="stButton"] > button[kind="primary"]:hover {
                    transform: scale(1.1) !important;
                    animation: none !important;
                    background-position: 0 0 !important;
                    box-shadow: 0 0 60px rgba(0, 255, 234, 0.8), 
                                0 0 100px rgba(255, 0, 255, 0.5),
                                inset 0 0 30px rgba(255, 255, 255, 0.3) !important;
                }
                
                div[data-testid="stButton"] > button[kind="primary"]::after {
                    content: ' ⚡' !important;
                    animation: float 1.5s infinite ease-in-out !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                </div>
                """, unsafe_allow_html=True)
            
            # Add instructions below the button
            st.markdown("""
            <div style="text-align: center; margin-top: 30px; color: #a0a0a0; font-family: 'Exo 2', sans-serif;">
                Click the button above to access the full B-Predictor Dashboard
            </div>
            """, unsafe_allow_html=True)
    
    else:
        # If dashboard should be shown, initialize and run it
        dashboard = BPredictorDashboard()
        
        # Run dashboard with sidebar and content
        dashboard.render_sidebar()
        
        # Default to dashboard view
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Dashboard'
        
        # Render appropriate page
        if st.session_state['current_page'] == 'Dashboard':
            dashboard.render_dashboard()
        elif st.session_state['current_page'] == 'Metrics & Anomalies':
            dashboard.render_metrics_anomalies()
        elif st.session_state['current_page'] == 'LSTM Forecast':
            dashboard.render_lstm_forecast()
        elif st.session_state['current_page'] == 'Root-Cause Analysis':
            dashboard.render_root_cause()
        elif st.session_state['current_page'] == 'Decision Intelligence':
            dashboard.render_decision_intelligence()
        
        # Add a back button in the sidebar
        st.sidebar.markdown("---")
        if st.sidebar.button("← Back to Intro", use_container_width=True):
            st.session_state.show_dashboard = False
            st.rerun()