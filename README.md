🧠 B-Predictor AI Dashboard

B-Predictor is an AI-powered platform for system monitoring, anomaly detection, incident prediction, and root-cause analysis.
It provides interactive dashboards, LSTM-based forecasting, SHAP explanations, and decision intelligence recommendations with a modern, animated interface.

🚀 Features

🏠 Animated Landing Page
Glowing header with particle animation background.

📊 Metrics & Anomaly Detection
Real-time visualization of CPU, memory, disk, network, and error metrics. Detect anomalies using pre-trained ML models.

📈 LSTM Incident Forecasting
Predict system incidents with probability charts using LSTM models.

🔍 Root-Cause Analysis (SHAP)
Identify key contributing features to anomalies and incidents.

🛠 Decision Intelligence
Recommended fixes and severity analysis for system anomalies.

🌌 Modern UI/UX
Dark mode, animated headers, cards, and particle backgrounds for a professional dashboard experience.

📦 Installation

Clone the repository:

git clone https://github.com/yourusername/b-predictor.git
cd b-predictor


Create and activate a virtual environment:

python -m venv venv
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


Prepare models:

models/anomaly_model.pkl

models/lstm_model.h5

Add your metrics data in CSV format: data/metrics.csv

Run the dashboard:

streamlit run src/dashboard.py

⚙️ Folder Structure
<img width="381" height="687" alt="image" src="https://github.com/user-attachments/assets/4b6bed0f-0c39-4484-837e-bea3a1193c6a" />

📊 Technology Stack

Python 3.10+

Streamlit – Interactive dashboard

Plotly – Charts & visualizations

TensorFlow / Keras – LSTM model

Pickle – Anomaly detection model

SHAP – Explainable AI

tsParticles – Landing page particle animation

🔧 Usage

Open the dashboard in your browser.

Navigate using the sidebar:

Home – Overview.

Metrics & Anomalies – Visualize metrics and detect anomalies.

LSTM Forecast – Incident predictions.

Root-Cause Analysis – SHAP explanations.

Decision Intelligence – Recommended actions.

Ensure models are loaded before using forecasting or root-cause analysis.

🎯 Future Improvements

Connect to live device metrics (Prometheus, APIs, IoT sensors).

Enhanced particle animation effects on landing page.

User authentication for enterprise usage.

Advanced dashboard theming and animations.

📌 Notes

Ensure metrics.csv contains at least 10 rows for LSTM forecasting.

Columns required: timestamp, cpu_usage, memory_usage, disk_io, network_latency, error_rate.

📂 Screenshots

<img width="1853" height="875" alt="Screenshot 2025-12-24 001227" src="https://github.com/user-attachments/assets/d854fbd8-c9a5-49c8-abfa-02c74cdd6424" />
<img width="1859" height="917" alt="Screenshot 2025-12-24 001423" src="https://github.com/user-attachments/assets/44f98761-6541-403e-8704-6ae4d4fd51a4" />
<img width="1855" height="896" alt="Screenshot 2025-12-24 001447" src="https://github.com/user-attachments/assets/bdeef9de-15ac-45e6-899d-31edf8366aca" />
<img width="1857" height="910" alt="Screenshot 2025-12-24 001503" src="https://github.com/user-attachments/assets/ccf8e4c8-8b8f-4f74-9717-944a79077461" />
<img width="1857" height="920" alt="Screenshot 2025-12-24 001518" src="https://github.com/user-attachments/assets/414fdae7-163a-449c-a989-a158a6f55eed" />
<img width="1862" height="905" alt="Screenshot 2025-12-24 001534" src="https://github.com/user-attachments/assets/d9b4fb94-e1e8-43de-9ff5-f5753c5ad644" />

#### Demo Video (3-minutes Demo )
click to watch demo ( <" https://docs.google.com/videos/d/1GRKPj-2EQr-0usl01ov_5a12MUarfSZB5Bykd4-vieg/edit?usp=sharing" >)








💡 Author

Bongu Rishi

AI & ML Engineer | Creator of B-Predictor
Founder of B = MY BLOOD MY DREAM MY LEGACY
Portfolio: https://rishibongu.com
