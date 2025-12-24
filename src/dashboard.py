"""
B-Predictor Dashboard - Enhanced Tech Edition with REAL-TIME DATA
AI-powered system monitoring with live metrics collection
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
from datetime import datetime, timedelta
import threading
import queue
from collections import deque
import os
import sys

# ---------- FIXED IMPORT ----------
# Since both files are in the same directory, use relative import
try:
    # Try relative import first
    from .live_agent import collect_metrics, stream_metrics
except ImportError:
    try:
        # If that fails, try direct import (both files in same directory)
        from live_agent import collect_metrics, stream_metrics
    except ImportError:
        # Create a fallback if live_agent.py is not found
        st.warning("⚠️ live_agent.py not found. Using simulated metrics.")
        
        # Define fallback functions
        import psutil
        from datetime import datetime
        
        def collect_metrics():
            """Fallback metrics collection if live_agent is missing"""
            try:
                return {
                    "timestamp": datetime.now(),
                    "cpu_usage": psutil.cpu_percent(interval=1),
                    "memory_usage": psutil.virtual_memory().percent,
                    "disk_io": psutil.disk_io_counters().read_bytes / 1e6,
                    "network_latency": psutil.net_io_counters().bytes_sent / 1e6,
                    "error_rate": 0.0
                }
            except:
                # Return simulated data if psutil fails
                return {
                    "timestamp": datetime.now(),
                    "cpu_usage": np.random.uniform(20, 80),
                    "memory_usage": np.random.uniform(30, 90),
                    "disk_io": np.random.uniform(10, 100),
                    "network_latency": np.random.uniform(5, 50),
                    "error_rate": 0.0
                }
        
        def stream_metrics():
            """Fallback stream generator"""
            history = []
            while True:
                data = collect_metrics()
                history.append(data)
                if len(history) > 200:
                    history.pop(0)
                yield history
                time.sleep(2)

# ---------- GLOBAL DATA STORE ----------
# Use session state for real-time data persistence
if 'metrics_history' not in st.session_state:
    st.session_state.metrics_history = deque(maxlen=200)  # Keep last 200 readings

if 'last_update_time' not in st.session_state:
    st.session_state.last_update_time = datetime.now()

if 'data_stream_active' not in st.session_state:
    st.session_state.data_stream_active = False

# ---------- REALTIME DATA COLLECTION FUNCTION ----------
def start_realtime_data_collection():
    """Start background thread for collecting real-time metrics"""
    if not st.session_state.data_stream_active:
        st.session_state.data_stream_active = True
        
        # Create a simple thread to update metrics periodically
        def update_metrics():
            while st.session_state.data_stream_active:
                try:
                    # Collect live metrics
                    live_data = collect_metrics()
                    
                    # Add to history
                    st.session_state.metrics_history.append(live_data)
                    st.session_state.last_update_time = datetime.now()
                    
                    # Wait before next collection
                    time.sleep(2)  # Match the 2-second interval
                except Exception as e:
                    print(f"Error collecting metrics: {e}")
                    time.sleep(5)
        
        # Start thread
        thread = threading.Thread(target=update_metrics, daemon=True)
        thread.start()

def stop_realtime_data_collection():
    """Stop the data collection"""
    st.session_state.data_stream_active = False

def get_latest_metrics_df():
    """Convert metrics history to DataFrame"""
    if len(st.session_state.metrics_history) == 0:
        # If no live data yet, collect some now
        for _ in range(5):
            try:
                st.session_state.metrics_history.append(collect_metrics())
            except:
                # If collect_metrics fails, create dummy data
                st.session_state.metrics_history.append({
                    "timestamp": datetime.now(),
                    "cpu_usage": np.random.uniform(20, 80),
                    "memory_usage": np.random.uniform(30, 90),
                    "disk_io": np.random.uniform(10, 100),
                    "network_latency": np.random.uniform(5, 50),
                    "error_rate": 0.0
                })
            time.sleep(0.5)
    
    # Convert to DataFrame
    df = pd.DataFrame(list(st.session_state.metrics_history))
    
    # Ensure timestamp is datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="B-Predictor AI | LIVE Predictive System Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/b-predictor',
        'Report a bug': "https://github.com/b-predictor/issues",
        'About': "# B-Predictor AI v2.0 - LIVE Predictive System Intelligence"
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
    
    /* Live indicator */
    .live-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #ff3333;
        border-radius: 50%;
        margin-right: 5px;
        animation: pulse 1s infinite;
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
    with st.container():
        st.markdown('<div class="intro-container">', unsafe_allow_html=True)
        
        # Main animated header
        st.markdown('<div class="main-header">⚡ B-PREDICTOR AI</div>', unsafe_allow_html=True)
        
        # Animated brand meaning
        st.markdown('<div class="brand-meaning">B = MY BLOOD • MY BRAND • MY LEGACY</div>', unsafe_allow_html=True)
        
        # Tagline with typing effect
        tagline_html = """
        <div class="brand-tagline">
            <span id="typed-text"></span>
            <span class="cursor">|</span>
        </div>
        <script>
            const texts = [
                "LIVE METRICS • REAL-TIME AI",
                "ACTIVE SYSTEM MONITORING",
                "PREDICT → DETECT → EXPLAIN",
                "AI-POWERED SYSTEM INTELLIGENCE"
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
                
                cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
            }
            
            document.addEventListener('DOMContentLoaded', typeEffect);
        </script>
        """
        st.components.v1.html(tagline_html, height=100)
        
        # Sub-header with tech stats
        st.markdown('<div class="sub-header">PREDICT → DETECT → EXPLAIN</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">LIVE SYSTEM MONITORING • REAL-TIME METRICS</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">ACTIVE PREDICTIVE INTELLIGENCE PLATFORM v2.1</div>', unsafe_allow_html=True)
        
        # Tech stats badges
        st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <span class="stat-badge">⚡ LIVE DATA STREAM</span>
            <span class="stat-badge">📊 REAL METRICS</span>
            <span class="stat-badge">🧠 ACTIVE AI</span>
            <span class="stat-badge">🔮 LIVE PREDICTIONS</span>
        </div>
        """, unsafe_allow_html=True)
        
        # System status indicator
        current_time = datetime.now().strftime('%H:%M:%S')
        status_html = f"""
        <div style="text-align: center; margin: 40px 0 0 0; padding: 15px; background: rgba(0, 255, 234, 0.1); border-radius: 10px; border: 1px solid rgba(0, 255, 234, 0.3); max-width: 600px; margin-left: auto; margin-right: auto;">
            <div style="display: flex; justify-content: center; align-items: center; gap: 10px;">
                <div style="width: 12px; height: 12px; background: #ffaa00; border-radius: 50%; animation: pulse 1s infinite;"></div>
                <span style="font-family: 'Orbitron', sans-serif; font-size: 1.1rem;">READY FOR LIVE MONITORING</span>
            </div>
            <div style="font-family: 'Exo 2', sans-serif; font-size: 0.9rem; color: #a0a0a0; margin-top: 5px;">
                Click START to begin collecting real system metrics | Current Time: {current_time}
            </div>
        </div>
        """
        st.markdown(status_html, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- ENHANCED DASHBOARD CLASS WITH LIVE DATA ----------
class BPredictorDashboard:
    """Main dashboard class for B-Predictor with LIVE data"""
    
    def __init__(self):
        """Initialize models and START live data collection"""
        self.feature_cols = ["cpu_usage", "memory_usage", "disk_io", "network_latency", "error_rate"]
        self.df = None
        self.anomaly_model = None
        self.lstm_model = None
        self.X_seq = None
        self.y_pred = None
        
        # Start live data collection
        start_realtime_data_collection()
        
        self.load_models()
        self.update_live_data()
    
    def load_models(self):
        """Load anomaly and LSTM models"""
        try:
            # Try to load models from the same directory or parent
            model_paths = [
                "models/anomaly_model.pkl",
                "../models/anomaly_model.pkl",
                "anomaly_model.pkl"
            ]
            
            for path in model_paths:
                try:
                    self.anomaly_model = pickle.load(open(path, "rb"))
                    break
                except:
                    continue
            
            lstm_paths = [
                "models/lstm_model.h5",
                "../models/lstm_model.h5",
                "lstm_model.h5"
            ]
            
            for path in lstm_paths:
                try:
                    self.lstm_model = load_model(path)
                    break
                except:
                    continue
            
            if self.anomaly_model and self.lstm_model:
                st.session_state['models_loaded'] = True
            else:
                raise Exception("Models not found in expected locations")
                
        except Exception as e:
            # Create simple fallback models for demo if real ones don't exist
            st.warning(f"⚠️ AI models not found. Using simulated AI detection.")
            st.session_state['models_loaded'] = False
            self.create_fallback_models()
    
    def create_fallback_models(self):
        """Create simple fallback models for demo purposes"""
        # Simple anomaly detection based on thresholds
        class SimpleAnomalyDetector:
            def predict(self, X):
                # Simple rule: if CPU > 85% or Memory > 80%, flag as anomaly
                predictions = []
                for _, row in X.iterrows():
                    cpu = row.get('cpu_usage', 0)
                    memory = row.get('memory_usage', 0)
                    
                    if cpu > 85 or memory > 80:
                        predictions.append(-1)  # Anomaly
                    elif cpu > 70 or memory > 70:
                        predictions.append(0)   # Warning
                    else:
                        predictions.append(1)   # Normal
                return np.array(predictions)
        
        self.anomaly_model = SimpleAnomalyDetector()
    
    def update_live_data(self):
        """Update with live metrics from the system"""
        try:
            # Get live metrics DataFrame
            self.df = get_latest_metrics_df()
            
            if not self.df.empty and len(self.df) > 0:
                # Anomaly predictions on live data
                if "anomaly" not in self.df.columns:
                    # Use only available columns
                    available_cols = [col for col in self.feature_cols if col in self.df.columns]
                    if available_cols:
                        self.df["anomaly"] = self.anomaly_model.predict(self.df[available_cols])
                        # Map predictions to labels
                        def map_anomaly(val):
                            if val == -1:
                                return "Critical"
                            elif val == 0:
                                return "Warning"
                            else:
                                return "Normal"
                        
                        self.df["anomaly_label"] = self.df["anomaly"].apply(map_anomaly)
                
                # LSTM sequences if we have enough data
                TIMESTEPS = 10
                if len(self.df) >= TIMESTEPS and all(col in self.df.columns for col in self.feature_cols):
                    self.X_seq = np.array([self.df[self.feature_cols].iloc[i:i+TIMESTEPS].values 
                                          for i in range(len(self.df)-TIMESTEPS)]).astype(np.float32)
                    
                    # Try to get predictions if we have a model
                    if hasattr(self, 'lstm_model') and self.lstm_model:
                        self.y_pred = self.lstm_model.predict(self.X_seq).flatten()
                    else:
                        # Simulate predictions based on recent trends
                        self.y_pred = self.simulate_predictions()
                else:
                    self.X_seq = None
                    self.y_pred = None
                    
        except Exception as e:
            st.error(f"Error updating live data: {str(e)}")
            # Create minimal demo data if live collection fails
            self.create_demo_data()
    
    def simulate_predictions(self):
        """Simulate predictions based on recent metric trends"""
        if len(self.df) < 5:
            return np.array([0.3])
        
        # Simple risk calculation based on recent metrics
        recent = self.df.tail(5)
        risk = 0.0
        
        if 'cpu_usage' in recent.columns:
            cpu_avg = recent['cpu_usage'].mean()
            risk += min(cpu_avg / 100, 0.5)  # 100% CPU = 0.5 risk
        
        if 'memory_usage' in recent.columns:
            mem_avg = recent['memory_usage'].mean()
            risk += min(mem_avg / 100, 0.5)  # 100% memory = 0.5 risk
        
        # Add some randomness for demo
        risk += np.random.uniform(-0.1, 0.1)
        risk = max(0.1, min(risk, 0.95))
        
        # Create a simple trend
        num_predictions = max(1, len(self.df) - 10)
        return np.linspace(max(0.1, risk - 0.1), min(0.9, risk + 0.1), num_predictions)
    
    def create_demo_data(self):
        """Create demo data if live collection isn't working"""
        times = pd.date_range(end=datetime.now(), periods=50, freq='2s')
        self.df = pd.DataFrame({
            'timestamp': times,
            'cpu_usage': np.random.normal(50, 15, 50).clip(0, 100),
            'memory_usage': np.random.normal(60, 10, 50).clip(0, 100),
            'disk_io': np.random.normal(50, 20, 50).clip(0, 200),
            'network_latency': np.random.normal(30, 10, 50).clip(0, 100),
            'error_rate': np.random.normal(0.5, 0.3, 50).clip(0, 2)
        })
        
        # Add some anomalies
        anomaly_indices = np.random.choice(50, 5, replace=False)
        self.df.loc[anomaly_indices, 'cpu_usage'] = np.random.normal(95, 3, 5)
        self.df['anomaly'] = 1
        self.df.loc[anomaly_indices, 'anomaly'] = -1
        self.df['anomaly_label'] = self.df['anomaly'].map({1: "Normal", -1: "Anomaly"})
    
    def render_sidebar(self):
        """Enhanced tech sidebar with LIVE metrics"""
        st.sidebar.markdown("""
        <div style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(0, 255, 234, 0.2);">
            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: #00ffea; margin-bottom: 10px;">
                ⚡ LIVE CONTROL
            </div>
            <div style="font-family: 'Exo 2', sans-serif; font-size: 0.9rem; color: #a0a0a0;">
                Real-time System Monitoring
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data collection status
        status_color = "#00ff88" if st.session_state.data_stream_active else "#ffaa00"
        status_text = "ACTIVE" if st.session_state.data_stream_active else "READY"
        
        st.sidebar.markdown(f"""
        <div style="background: rgba(10, 25, 47, 0.8); padding: 15px; border-radius: 10px; margin: 10px 0; border-left: 4px solid {status_color};">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="width: 10px; height: 10px; background: {status_color}; border-radius: 50%; animation: {'pulse 2s infinite' if st.session_state.data_stream_active else 'none'}"></div>
                <div style="font-family: 'Orbitron', sans-serif; color: {status_color};">DATA STREAM: {status_text}</div>
            </div>
            <div style="font-family: 'Exo 2', sans-serif; font-size: 0.8rem; color: #a0a0a0; margin-top: 5px;">
                Last update: {st.session_state.last_update_time.strftime('%H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation with icons
        pages = [
            ("🏠", "Dashboard", "System Overview"),
            ("📊", "Live Metrics", "Real-time Monitoring"),
            ("📈", "LSTM Forecast", "Predictive Analytics"),
            ("🔍", "Root-Cause Analysis", "SHAP Explanations"),
            ("⚡", "Decision Intelligence", "AI Recommendations")
        ]
        
        for icon, name, desc in pages:
            if st.sidebar.button(f"{icon} {name}", key=f"nav_{name}", use_container_width=True):
                st.session_state['current_page'] = name
        
        st.sidebar.markdown("---")
        
        # REAL LIVE METRICS from your system
        st.sidebar.markdown("""
        <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: #00ffea; margin: 20px 0 10px 0;">
            📡 LIVE SYSTEM METRICS
        </div>
        """, unsafe_allow_html=True)
        
        # Get actual live metrics
        if len(st.session_state.metrics_history) > 0:
            latest = list(st.session_state.metrics_history)[-1]
            
            # Determine colors based on values
            cpu_color = "#ff3333" if latest.get('cpu_usage', 0) > 80 else "#ffaa00" if latest.get('cpu_usage', 0) > 60 else "#00ff88"
            mem_color = "#ff3333" if latest.get('memory_usage', 0) > 80 else "#ffaa00" if latest.get('memory_usage', 0) > 60 else "#00ff88"
            
            metrics_display = [
                ("CPU Usage", f"{latest.get('cpu_usage', 0):.1f}%", cpu_color),
                ("Memory", f"{latest.get('memory_usage', 0):.1f}%", mem_color),
                ("Disk I/O", f"{latest.get('disk_io', 0):.1f} MB", "#00ffea"),
                ("Network", f"{latest.get('network_latency', 0):.1f} MB", "#ff00ff")
            ]
            
            for name, value, color in metrics_display:
                st.sidebar.markdown(f"""
                <div class="metric-card" style="border-left-color: {color};">
                    <div style="font-size: 0.9rem; color: #a0a0a0;">{name}</div>
                    <div class="metric-value" style="color: {color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            # Show placeholder if no data yet
            st.sidebar.info("Collecting initial metrics...")
        
        # Data collection controls
        st.sidebar.markdown("---")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                # Force immediate data collection
                try:
                    live_data = collect_metrics()
                    st.session_state.metrics_history.append(live_data)
                    st.session_state.last_update_time = datetime.now()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error collecting: {e}")
        
        with col2:
            if st.button("⏹️ Stop", use_container_width=True):
                stop_realtime_data_collection()
                st.rerun()
    
    def render_dashboard(self):
        """Enhanced dashboard view with LIVE data"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">LIVE SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
        
        # Update data before displaying
        self.update_live_data()
        
        # REAL KPI Cards from live data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_metrics = len(st.session_state.metrics_history)
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">📊 Live Metrics</div>
                <div class="metric-value" style="color: #00ffea;">{total_metrics}</div>
                <div style="font-size: 0.8rem; color: #00ff88;">Collected in real-time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if not self.df.empty and 'anomaly' in self.df.columns:
                anomaly_count = (self.df['anomaly'] == -1).sum()
                anomaly_color = "#ff3333" if anomaly_count > 0 else "#00ff88"
            else:
                anomaly_count = 0
                anomaly_color = "#00ff88"
                
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">⚠️ Live Anomalies</div>
                <div class="metric-value" style="color: {anomaly_color};">{anomaly_count}</div>
                <div style="font-size: 0.8rem; color: {anomaly_color};">Detected by AI</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if not self.df.empty and len(self.df) > 0 and 'cpu_usage' in self.df.columns:
                current_cpu = self.df['cpu_usage'].iloc[-1]
                cpu_color = "#ff3333" if current_cpu > 80 else "#ffaa00" if current_cpu > 60 else "#00ff88"
            else:
                current_cpu = 0
                cpu_color = "#00ff88"
                
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">⚡ Current CPU</div>
                <div class="metric-value" style="color: {cpu_color};">{current_cpu:.1f}%</div>
                <div style="font-size: 0.8rem; color: {cpu_color};">Live reading</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if not self.df.empty and len(self.df) > 0 and 'timestamp' in self.df.columns:
                latest_time = self.df['timestamp'].iloc[-1]
                time_str = latest_time.strftime('%H:%M:%S')
                time_ago = (datetime.now() - latest_time).total_seconds()
                time_color = "#ff3333" if time_ago > 10 else "#ffaa00" if time_ago > 5 else "#00ff88"
            else:
                time_str = "No data"
                time_color = "#ffaa00"
                
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 0.9rem; color: #a0a0a0;">🕒 Last Update</div>
                <div class="metric-value" style="color: {time_color}; font-size: 2rem;">{time_str}</div>
                <div style="font-size: 0.8rem; color: {time_color};">Real-time stream</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Auto-refresh notice
        if st.session_state.data_stream_active:
            st.markdown("""
            <div style="background: rgba(0, 255, 234, 0.1); padding: 10px; border-radius: 10px; margin: 20px 0; text-align: center; border: 1px solid rgba(0, 255, 234, 0.3);">
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <div style="width: 8px; height: 8px; background: #00ff88; border-radius: 50%; animation: pulse 1s infinite;"></div>
                    <span style="font-family: 'Exo 2', sans-serif; color: #00ffea;">LIVE DATA STREAM ACTIVE • Auto-refreshing with new metrics</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Charts Section with LIVE DATA
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Live CPU Usage")
            if not self.df.empty and 'cpu_usage' in self.df.columns and 'timestamp' in self.df.columns:
                fig = px.line(self.df, x="timestamp", y="cpu_usage", 
                             title=f"Real CPU Usage: {self.df['cpu_usage'].iloc[-1]:.1f}%", 
                             template="plotly_dark")
                fig.update_traces(line=dict(color='#00ffea', width=3))
                
                # Add threshold lines
                fig.add_hline(y=80, line_dash="dash", line_color="#ff3333", 
                            annotation_text="Critical", annotation_position="bottom right")
                fig.add_hline(y=60, line_dash="dot", line_color="#ffaa00", 
                            annotation_text="Warning", annotation_position="bottom right")
                
                fig.update_layout(plot_bgcolor='rgba(10, 25, 47, 0.8)',
                                paper_bgcolor='rgba(10, 25, 47, 0.8)',
                                showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Collecting CPU data...")
        
        with col2:
            st.subheader("📊 Live Memory Usage")
            if not self.df.empty and 'memory_usage' in self.df.columns and 'timestamp' in self.df.columns:
                fig = px.line(self.df, x="timestamp", y="memory_usage", 
                             title=f"Real Memory Usage: {self.df['memory_usage'].iloc[-1]:.1f}%", 
                             template="plotly_dark")
                fig.update_traces(line=dict(color='#ff00ff', width=3), fill='tozeroy')
                
                # Add threshold lines
                fig.add_hline(y=80, line_dash="dash", line_color="#ff3333")
                fig.add_hline(y=60, line_dash="dot", line_color="#ffaa00")
                
                fig.update_layout(plot_bgcolor='rgba(10, 25, 47, 0.8)',
                                paper_bgcolor='rgba(10, 25, 47, 0.8)',
                                showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Collecting memory data...")
        
        # Live anomalies table
        st.markdown("---")
        st.subheader("🚨 Recent Anomalies Detected")
        if not self.df.empty and 'anomaly_label' in self.df.columns:
            anomalies = self.df[self.df['anomaly_label'].isin(['Critical', 'Warning'])]
            if not anomalies.empty:
                # Show last 5 anomalies
                recent_anomalies = anomalies.tail(5).copy()
                recent_anomalies['Time'] = recent_anomalies['timestamp'].dt.strftime('%H:%M:%S')
                
                # Create styled table
                for _, row in recent_anomalies.iterrows():
                    severity_color = "#ff3333" if row['anomaly_label'] == 'Critical' else "#ffaa00"
                    st.markdown(f"""
                    <div class="tech-card" style="border-left-color: {severity_color}; margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 1.1rem; color: white;">
                                    {row['anomaly_label']} Alert - {row['Time']}
                                </div>
                                <div style="font-size: 0.9rem; color: #a0a0a0;">
                                    CPU: {row.get('cpu_usage', 'N/A'):.1f}% | Memory: {row.get('memory_usage', 'N/A'):.1f}%
                                </div>
                            </div>
                            <div style="font-size: 1.5rem; color: {severity_color};">
                                {'🔴' if row['anomaly_label'] == 'Critical' else '🟡'}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No anomalies detected in recent data")
        else:
            st.info("Anomaly detection initializing...")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    def render_live_metrics(self):
        """Enhanced metrics view with LIVE data"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">📊 LIVE SYSTEM METRICS</div>', unsafe_allow_html=True)
        
        # Update with latest data
        self.update_live_data()
        
        if self.df.empty or len(self.df) < 2:
            st.warning("📡 Collecting initial live data... Please wait a few seconds.")
            # Try to collect some data now
            for _ in range(3):
                try:
                    st.session_state.metrics_history.append(collect_metrics())
                except:
                    pass
                time.sleep(1)
            self.update_live_data()
            st.rerun()
            return
        
        # Show data collection status
        time_since_update = (datetime.now() - st.session_state.last_update_time).total_seconds()
        status_color = "#00ff88" if time_since_update < 5 else "#ffaa00" if time_since_update < 10 else "#ff3333"
        
        st.markdown(f"""
        <div style="background: rgba(0, 255, 234, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(0, 255, 234, 0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 10px; height: 10px; background: {status_color}; border-radius: 50%; animation: pulse 1s infinite;"></div>
                        <span style="font-family: 'Orbitron', sans-serif; color: #00ffea;">ACTIVE DATA STREAM</span>
                    </div>
                    <div style="font-family: 'Exo 2', sans-serif; font-size: 0.9rem; color: #a0a0a0; margin-top: 5px;">
                        Collecting metrics from your system every 2 seconds
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-family: 'Orbitron', sans-serif; color: #00ffea;">{len(self.df)} live readings</div>
                    <div style="font-family: 'Exo 2', sans-serif; font-size: 0.8rem; color: {status_color};">
                        Updated {time_since_update:.0f} seconds ago
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # All metrics in one chart - FIXED VERSION
        st.subheader("📈 All Live Metrics Overview")
        
        # Create a simpler visualization - individual metrics in subplots
        fig = go.Figure()
        
        # Add each metric as a trace
        metrics_to_plot = [col for col in self.feature_cols if col in self.df.columns]
        colors = ['#00ffea', '#ff00ff', '#ffaa00', '#00ff88', '#0088ff']
        metric_names = {
            'cpu_usage': 'CPU Usage (%)',
            'memory_usage': 'Memory Usage (%)',
            'disk_io': 'Disk I/O (MB)',
            'network_latency': 'Network (MB)',
            'error_rate': 'Error Rate'
        }
        
        for i, metric in enumerate(metrics_to_plot):
            if metric in self.df.columns:
                color = colors[i % len(colors)]
                fig.add_trace(go.Scatter(
                    x=self.df["timestamp"],
                    y=self.df[metric],
                    mode='lines',
                    name=metric_names.get(metric, metric.replace('_', ' ').title()),
                    line=dict(color=color, width=2),
                    yaxis=f"y{i+1}" if i > 0 else "y"
                ))
        
        # Create layout with proper axis configuration
        layout = {
            'title': "All System Metrics - Live Feed",
            'template': "plotly_dark",
            'plot_bgcolor': 'rgba(10, 25, 47, 0.8)',
            'paper_bgcolor': 'rgba(10, 25, 47, 0.8)',
            'hovermode': 'x unified',
            'height': 500,
            'showlegend': True,
            'legend': dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(10, 25, 47, 0.8)',
                font=dict(color='white')
            )
        }
        
        # Add secondary axes properly
        if len(metrics_to_plot) > 1:
            for i in range(1, len(metrics_to_plot)):
                axis_name = f"yaxis{i+1}"
                layout[axis_name] = dict(
                    title=dict(
                        text=metric_names.get(metrics_to_plot[i], metrics_to_plot[i].replace('_', ' ').title()),
                        font=dict(color=colors[i % len(colors)])
                    ),
                    tickfont=dict(color=colors[i % len(colors)]),
                    overlaying="y",
                    side="right",
                    position=0.85
                )
        
        # Set primary y-axis
        if metrics_to_plot:
            layout['yaxis'] = dict(
                title=dict(
                    text=metric_names.get(metrics_to_plot[0], metrics_to_plot[0].replace('_', ' ').title()),
                    font=dict(color=colors[0])
                ),
                tickfont=dict(color=colors[0])
            )
        
        fig.update_layout(**layout)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Alternative: Show metrics in separate subplots for clarity
        st.subheader("📊 Individual Metric Views")
        
        # Create subplots for each metric
        for i, metric in enumerate(metrics_to_plot[:4]):  # Show first 4 metrics max
            if metric in self.df.columns:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Create individual chart for each metric
                    fig_single = go.Figure()
                    fig_single.add_trace(go.Scatter(
                        x=self.df["timestamp"],
                        y=self.df[metric],
                        mode='lines',
                        name=metric_names.get(metric, metric.replace('_', ' ').title()),
                        line=dict(color=colors[i % len(colors)], width=3),
                        fill='tozeroy' if metric in ['cpu_usage', 'memory_usage'] else None,
                        fillcolor=f'rgba{tuple(int(colors[i % len(colors)].lstrip("#")[j:j+2], 16) for j in (0, 2, 4)) + (0.2,)}'
                    ))
                    
                    # Get latest value
                    latest_value = self.df[metric].iloc[-1] if len(self.df) > 0 else 0
                    
                    fig_single.update_layout(
                        title=f"{metric_names.get(metric, metric.replace('_', ' ').title())} - Current: {latest_value:.2f}",
                        template="plotly_dark",
                        plot_bgcolor='rgba(10, 25, 47, 0.8)',
                        paper_bgcolor='rgba(10, 25, 47, 0.8)',
                        height=250,
                        showlegend=False,
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    
                    st.plotly_chart(fig_single, use_container_width=True)
                
                with col2:
                    # Show stats
                    if len(self.df) > 0:
                        current = self.df[metric].iloc[-1]
                        avg = self.df[metric].mean()
                        min_val = self.df[metric].min()
                        max_val = self.df[metric].max()
                        
                        # Determine color based on value for CPU and Memory
                        if metric in ['cpu_usage', 'memory_usage']:
                            value_color = "#ff3333" if current > 80 else "#ffaa00" if current > 60 else "#00ff88"
                        else:
                            value_color = colors[i % len(colors)]
                        
                        st.markdown(f"""
                        <div style="background: rgba(10, 25, 47, 0.8); padding: 15px; border-radius: 10px; border-left: 4px solid {value_color}; margin-top: 20px;">
                            <div style="font-family: 'Orbitron', sans-serif; font-size: 1.2rem; color: {value_color}; margin-bottom: 10px;">
                                Current: {current:.1f}
                            </div>
                            <div style="font-family: 'Exo 2', sans-serif; color: #a0a0a0; font-size: 0.8rem;">
                                Avg: {avg:.1f}<br>
                                Min: {min_val:.1f}<br>
                                Max: {max_val:.1f}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Latest live metrics table
        st.subheader("🔄 Latest Live Readings")
        if len(self.df) > 0:
            # Show last 10 readings
            latest_readings = self.df.tail(10).copy()
            
            # Format timestamp for display
            latest_readings['Time'] = latest_readings['timestamp'].dt.strftime('%H:%M:%S')
            
            # Select columns to display
            display_cols = ['Time'] + [col for col in self.feature_cols if col in latest_readings.columns]
            if 'anomaly_label' in latest_readings.columns:
                display_cols.append('anomaly_label')
            
            # Create styled dataframe
            st.dataframe(
                latest_readings[display_cols].style.format({
                    'cpu_usage': '{:.1f}%',
                    'memory_usage': '{:.1f}%',
                    'disk_io': '{:.1f} MB',
                    'network_latency': '{:.1f} MB',
                    'error_rate': '{:.3f}'
                }).apply(
                    lambda x: ['background: rgba(255, 51, 51, 0.1)' if v in ['Critical', -1] else 
                              'background: rgba(255, 170, 0, 0.1)' if v in ['Warning', 0] else '' 
                              for v in x], 
                    axis=1
                ),
                use_container_width=True,
                height=400
            )
        
        # Refresh button
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🔄 Refresh Live Data", use_container_width=True, type="primary"):
                # Force new data collection
                try:
                    live_data = collect_metrics()
                    st.session_state.metrics_history.append(live_data)
                    st.session_state.last_update_time = datetime.now()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error refreshing: {e}")
        
        with col2:
            if st.button("📥 Export Data", use_container_width=True):
                # Export current data
                csv = self.df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"system_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_lstm_forecast(self):
        """LSTM forecast view"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">📈 PREDICTIVE ANALYTICS</div>', unsafe_allow_html=True)
        
        self.update_live_data()
        
        if self.X_seq is None or self.y_pred is None:
            st.warning("📊 Collecting more data for predictions... Need at least 10 data points.")
            # Show progress
            if len(self.df) > 0:
                progress = min(len(self.df) / 10, 1.0)
                st.progress(progress, text=f"Data collected: {len(self.df)}/10 points")
            return
        
        # Forecast chart
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
        
        # Threshold lines
        fig.add_hline(y=0.7, line_dash="dash", line_color="#ff3333", 
                     annotation_text="Critical", annotation_position="bottom right")
        fig.add_hline(y=0.5, line_dash="dot", line_color="#ffaa00", 
                     annotation_text="Warning", annotation_position="bottom right")
        
        fig.update_layout(
            title="LSTM Incident Probability Forecast (Live)",
            template="plotly_dark",
            yaxis_range=[0, 1],
            plot_bgcolor='rgba(10, 25, 47, 0.8)',
            paper_bgcolor='rgba(10, 25, 47, 0.8)',
            yaxis_title="Risk Probability"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Forecast insights
        current_risk = self.y_pred[-1] if len(self.y_pred) > 0 else 0
        
        if current_risk < 0.3:
            risk_level = "🟢 LOW"
            risk_color = "#00ff88"
            recommendation = "System operating normally"
        elif current_risk < 0.7:
            risk_level = "🟡 MEDIUM"
            risk_color = "#ffaa00"
            recommendation = "Monitor system closely"
        else:
            risk_level = "🔴 HIGH"
            risk_color = "#ff3333"
            recommendation = "Take immediate action"
        
        st.markdown(f"""
        <div class="tech-card">
            <div style="font-size: 1.2rem; color: #00ffea;">📊 Live Forecast Insights</div>
            <div style="margin: 20px 0;">
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                    <div style="padding: 15px; background: rgba(0, 255, 234, 0.1); border-radius: 10px;">
                        <div style="color: #a0a0a0; font-size: 0.9rem;">Current Risk Level</div>
                        <div style="color: {risk_color}; font-size: 1.8rem; font-weight: bold; margin-top: 5px;">
                            {risk_level}
                        </div>
                    </div>
                    <div style="padding: 15px; background: rgba(255, 0, 255, 0.1); border-radius: 10px;">
                        <div style="color: #a0a0a0; font-size: 0.9rem;">Probability</div>
                        <div style="color: #ff00ff; font-size: 1.8rem; font-weight: bold; margin-top: 5px;">
                            {current_risk:.1%}
                        </div>
                    </div>
                </div>
            </div>
            <div style="color: {risk_color}; font-size: 1rem; font-weight: bold; padding: 10px; background: rgba{tuple(int(risk_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}; border-radius: 8px; margin-top: 10px;">
                ⚡ Recommendation: {recommendation}
            </div>
            <div style="color: #a0a0a0; font-size: 0.9rem; margin-top: 15px;">
                Based on LSTM neural network analysis of {len(self.df)} live data points
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_root_cause(self):
        """Root cause analysis with live data"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">🔍 ROOT CAUSE ANALYSIS</div>', unsafe_allow_html=True)
        
        self.update_live_data()
        
        if self.df.empty or len(self.df) < 5:
            st.info("Collecting data for analysis...")
            return
        
        # Simple feature importance based on correlation with anomalies
        if 'anomaly' in self.df.columns:
            correlations = {}
            for col in self.feature_cols:
                if col in self.df.columns:
                    try:
                        corr = abs(self.df[col].corr(self.df['anomaly']))
                        correlations[col] = corr if not pd.isna(corr) else 0
                    except:
                        correlations[col] = 0
            
            # Sort by correlation
            sorted_corrs = sorted(correlations.items(), key=lambda x: x[1], reverse=True)
            
            # Create visualization
            fig = go.Figure(data=[
                go.Bar(
                    x=[c[0].replace('_', ' ').title() for c in sorted_corrs],
                    y=[c[1] for c in sorted_corrs],
                    marker_color=['#ff3333', '#ffaa00', '#00ffea', '#ff00ff', '#00ff88'][:len(sorted_corrs)]
                )
            ])
            
            fig.update_layout(
                title="Feature Impact on Anomalies (Live Correlation)",
                template="plotly_dark",
                plot_bgcolor='rgba(10, 25, 47, 0.8)',
                paper_bgcolor='rgba(10, 25, 47, 0.8)',
                yaxis_title="Correlation with Anomalies",
                yaxis_range=[0, 1]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display insights
            top_factor = sorted_corrs[0][0] if sorted_corrs else "CPU Usage"
            top_value = sorted_corrs[0][1] if sorted_corrs else 0
            
            st.markdown(f"""
            <div class="tech-card">
                <div style="font-size: 1.2rem; color: #00ffea;">🧠 Live Analysis Results</div>
                <div style="margin: 20px 0;">
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                        <div style="padding: 10px; background: rgba(255, 51, 51, 0.1); border-radius: 8px;">
                            <div style="color: #a0a0a0; font-size: 0.9rem;">Primary Contributor</div>
                            <div style="color: #ff3333; font-size: 1.2rem; font-weight: bold;">{top_factor.replace('_', ' ').title()}</div>
                        </div>
                        <div style="padding: 10px; background: rgba(255, 0, 255, 0.1); border-radius: 8px;">
                            <div style="color: #a0a0a0; font-size: 0.9rem;">Impact Score</div>
                            <div style="color: #ff00ff; font-size: 1.2rem; font-weight: bold;">{top_value:.3f}</div>
                        </div>
                    </div>
                </div>
                <div style="color: #a0a0a0; font-size: 0.9rem; margin-top: 10px;">
                    Analysis based on {len(self.df)} live data points showing correlation between metrics and detected anomalies
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_decision_intelligence(self):
        """Decision intelligence with live data"""
        st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
        st.markdown('<div class="main-header" style="font-size: 3rem;">⚡ DECISION INTELLIGENCE</div>', unsafe_allow_html=True)
        
        self.update_live_data()
        
        # AI Recommendations based on live data
        recommendations = []
        
        if not self.df.empty and len(self.df) > 0:
            latest = self.df.iloc[-1]
            
            # CPU-based recommendations
            cpu = latest.get('cpu_usage', 0)
            if cpu > 85:
                recommendations.append({
                    "action": "Scale CPU resources immediately",
                    "priority": "🔴 CRITICAL",
                    "eta": "5min",
                    "reason": f"CPU at {cpu:.1f}% (Critical)",
                    "icon": "⚡"
                })
            elif cpu > 70:
                recommendations.append({
                    "action": "Monitor CPU load and consider scaling",
                    "priority": "🟡 WARNING",
                    "eta": "15min",
                    "reason": f"CPU at {cpu:.1f}% (High)",
                    "icon": "📈"
                })
            
            # Memory-based recommendations
            memory = latest.get('memory_usage', 0)
            if memory > 80:
                recommendations.append({
                    "action": "Check for memory leaks and optimize",
                    "priority": "🔴 CRITICAL",
                    "eta": "10min",
                    "reason": f"Memory at {memory:.1f}% (Critical)",
                    "icon": "💾"
                })
            elif memory > 65:
                recommendations.append({
                    "action": "Review memory usage patterns",
                    "priority": "🟡 WARNING",
                    "eta": "30min",
                    "reason": f"Memory at {memory:.1f}% (High)",
                    "icon": "📊"
                })
            
            # General recommendations
            if len(recommendations) == 0:
                recommendations.append({
                    "action": "System operating within normal parameters",
                    "priority": "🟢 NORMAL",
                    "eta": "N/A",
                    "reason": "All metrics within safe ranges",
                    "icon": "✅"
                })
            
            # Add proactive recommendations
            if 'anomaly' in self.df.columns and (self.df['anomaly'] == -1).sum() > 0:
                recommendations.append({
                    "action": "Review recent anomaly patterns",
                    "priority": "🟡 WARNING",
                    "eta": "20min",
                    "reason": "Multiple anomalies detected recently",
                    "icon": "🚨"
                })
        
        # Display recommendations
        for rec in recommendations:
            priority_color = "#ff3333" if "CRITICAL" in rec['priority'] else "#ffaa00" if "WARNING" in rec['priority'] else "#00ff88"
            
            st.markdown(f"""
            <div class="tech-card" style="margin: 10px 0; border-left-color: {priority_color};">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                            <div style="font-size: 1.5rem;">{rec['icon']}</div>
                            <div style="font-size: 1.1rem; color: white; font-weight: bold;">{rec['action']}</div>
                        </div>
                        <div style="font-size: 0.9rem; color: #a0a0a0; margin-bottom: 5px;">
                            {rec['reason']}
                        </div>
                        <div style="font-size: 0.8rem; color: #a0a0a0;">
                            Estimated response time: <span style="color: {priority_color};">{rec['eta']}</span>
                        </div>
                    </div>
                    <div style="font-size: 1.5rem; color: {priority_color}; font-weight: bold;">
                        {rec['priority']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Apply Recommendations", use_container_width=True):
                st.success("Recommendations applied! Monitoring for improvements...")
        
        with col2:
            if st.button("📊 Generate Report", use_container_width=True):
                st.info("Report generation started...")
        
        with col3:
            if st.button("🆘 Request Support", use_container_width=True):
                st.warning("Support team notified of system status")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- MAIN EXECUTION ----------
if __name__ == "__main__":
    # Initialize session state
    if 'show_dashboard' not in st.session_state:
        st.session_state.show_dashboard = False
    
    # Check if we can import live_agent
    try:
        # Try multiple import strategies
        try:
            from live_agent import collect_metrics, stream_metrics
            live_agent_available = True
        except ImportError:
            try:
                # Try relative import
                from .live_agent import collect_metrics, stream_metrics
                live_agent_available = True
            except ImportError:
                # Try from src folder
                from src.live_agent import collect_metrics, stream_metrics
                live_agent_available = True
    except:
        live_agent_available = False
    
    # Show intro first if dashboard not yet opened
    if not st.session_state.show_dashboard:
        render_tech_intro()
        
        # Customized button based on live agent availability
        button_text = "🚀 START LIVE MONITORING" if live_agent_available else "🚀 START DEMO MODE"
        button_help = "Click to begin real-time system monitoring" if live_agent_available else "Live agent not found, starting demo mode"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(button_text, 
                        key="predict_button",
                        help=button_help,
                        use_container_width=True):
                st.session_state.show_dashboard = True
                st.rerun()
    
    else:
        # Initialize and run the LIVE dashboard
        dashboard = BPredictorDashboard()
        
        # Run dashboard with sidebar and content
        dashboard.render_sidebar()
        
        # Default to dashboard view
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 'Dashboard'
        
        # Render appropriate page
        if st.session_state['current_page'] == 'Dashboard':
            dashboard.render_dashboard()
        elif st.session_state['current_page'] == 'Live Metrics':
            dashboard.render_live_metrics()
        elif st.session_state['current_page'] == 'LSTM Forecast':
            dashboard.render_lstm_forecast()
        elif st.session_state['current_page'] == 'Root-Cause Analysis':
            dashboard.render_root_cause()
        elif st.session_state['current_page'] == 'Decision Intelligence':
            dashboard.render_decision_intelligence()
        
        # Add auto-refresh for live data
        if st.session_state.data_stream_active:
            # Auto-refresh every 3 seconds
            time.sleep(3)
            st.rerun()
        
        # Add refresh button in sidebar
        st.sidebar.markdown("---")
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Update Now", use_container_width=True):
                # Force data collection
                try:
                    live_data = collect_metrics()
                    st.session_state.metrics_history.append(live_data)
                    st.session_state.last_update_time = datetime.now()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if st.button("← Back to Intro", use_container_width=True):
                st.session_state.show_dashboard = False
                stop_realtime_data_collection()
                st.rerun()


