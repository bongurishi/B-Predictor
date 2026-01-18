import streamlit as st

def show_landing():

    st.markdown("""
    <style>

    /* ===== ANIMATED BACKGROUND ===== */
    .stApp {
        background:
            radial-gradient(circle at 20% 20%, rgba(0,229,255,0.15), transparent 40%),
            radial-gradient(circle at 80% 30%, rgba(41,121,255,0.12), transparent 40%),
            radial-gradient(circle at 50% 80%, rgba(0,229,255,0.1), transparent 45%),
            #000000;
        background-size: 200% 200%;
        animation: bgMove 18s ease infinite;
    }

    @keyframes bgMove {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* ===== FLOATING PARTICLE OVERLAY ===== */
    .particle-layer {
        position: absolute;
        inset: 0;
        pointer-events: none;
        z-index: 0;
        background-image:
            radial-gradient(2px 2px at 20% 30%, #00e5ff 50%, transparent 51%),
            radial-gradient(1.5px 1.5px at 70% 40%, #ffffff 50%, transparent 51%),
            radial-gradient(1px 1px at 40% 70%, #00e5ff 50%, transparent 51%),
            radial-gradient(1.2px 1.2px at 85% 80%, #ffffff 50%, transparent 51%);
        background-size: 300px 300px;
        animation: particleDrift 25s linear infinite;
    }

    @keyframes particleDrift {
        from { background-position: 0 0; }
        to { background-position: 600px 1200px; }
    }

    /* ===== HERO ===== */
    .hero {
        position: relative;
        z-index: 2;
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        animation: fadeIn 1.8s ease;
        text-align: center;
    }

    .title {
        font-size: 4.5rem;
        font-weight: 800;
        color: #00e5ff;
        text-shadow: 0 0 30px #00e5ff;
        animation: glow 2s infinite alternate;
    }

    .subtitle {
        font-size: 1.4rem;
        color: #cfd8dc;
        margin-top: 8px;
    }

    .tagline {
        font-size: 2rem;
        margin: 18px 0;
        font-weight: 700;
        color: #00e5ff;
        letter-spacing: 1px;
    }

    .desc {
        max-width: 700px;
        color: #b0bec5;
        font-size: 18px;
        line-height: 1.6;
    }

    .btn {
        margin-top: 35px;
        padding: 14px 48px;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 30px;
        background: linear-gradient(90deg,#00e5ff,#2979ff);
        color: black;
        border: none;
        cursor: pointer;
        box-shadow: 0 0 35px #00e5ff;
        animation: pulse 2s infinite;
    }

    .btn:hover {
        transform: scale(1.08);
    }

    @keyframes glow {
        from { text-shadow: 0 0 15px #00e5ff; }
        to { text-shadow: 0 0 40px #00e5ff; }
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 20px #00e5ff; }
        50% { box-shadow: 0 0 45px #00e5ff; }
        100% { box-shadow: 0 0 20px #00e5ff; }
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(35px); }
        to { opacity: 1; transform: translateY(0); }
    }

    </style>
    """, unsafe_allow_html=True)

    # Particle overlay
    st.markdown('<div class="particle-layer"></div>', unsafe_allow_html=True)

    # Hero content
    st.markdown("""
    <div class="hero">
        <div class="title">B-Predictor</div>
        <div class="subtitle">My Blood • My Brand • My Legacy</div>
        <div class="tagline">Predict → Detect → Explain</div>
        <div class="desc">
            An AI system that predicts production incidents before they happen,
            explains root causes, and recommends actions like a senior engineer.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button(" Start Prediction"):
            st.session_state.started = True
            st.rerun()

