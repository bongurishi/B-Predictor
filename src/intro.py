import streamlit as st

def render_intro(
    title: str,
    subheading: str,
    tagline: str,
    started_state_key: str = "started"
):
    if not st.session_state.get(started_state_key, False):

        st.markdown("""
        <style>
        .intro-container {
            text-align: center;
            margin-top: 120px;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"<h1 class='intro-container'> {title}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='intro-container'>{subheading}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p class='intro-container'>{tagline}</p>", unsafe_allow_html=True)

        if st.button(" Start Prediction"):
            st.session_state[started_state_key] = True

        st.stop()

