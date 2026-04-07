from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

df = pd.read_csv("data.csv")

# ---------- METRICS ----------
def compute_metrics(signal, latency, speed):

    signal_norm = signal + 100
    speed_norm = speed * 2

    nqs = (0.4 * signal_norm) + (0.3 * speed_norm) - (0.3 * latency)
    nsi = 100 - np.std([signal, latency, speed])
    efficiency = speed / (latency + 1)
    packet_loss = latency / 200

    return round(nqs,2), round(nsi,2), round(efficiency,2), round(packet_loss,2)

# ---------- ROUTES ----------
@app.route('/')
def home():
    return "Network Intelligence API Running"

@app.route('/data')
def data():
    return df.to_json(orient="records")

@app.route('/predict', methods=['POST'])
def predict():
    d = request.json

    nqs, nsi, eff, loss = compute_metrics(
        d['signal_strength'], d['latency'], d['speed']
    )

    return jsonify({
        "NQS": nqs,
        "NSI": nsi,
        "Efficiency": eff,
        "PacketLoss": loss
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    d = request.json
    rec = []

    if d['signal_strength'] < -85:
        rec.append("Weak signal — move to open area")

    if d['latency'] > 100:
        rec.append("High latency — avoid peak hours")

    if d['speed'] < 10:
        rec.append("Low speed — switch network")

    return jsonify({"recommendations": rec})

@app.route('/insights', methods=['POST'])
def insights():
    d = request.json
    insights = []

    if d['latency'] > 80:
        insights.append("Network congestion detected")

    if d['signal_strength'] < -80:
        insights.append("Coverage issue detected")

    if d['speed'] < 15:
        insights.append("Bandwidth bottleneck observed")

    return jsonify({"insights": insights})

@app.route('/anomaly', methods=['POST'])
def anomaly():
    d = request.json
    prev = d.get("prev_nqs", 50)
    curr = d.get("current_nqs", 50)

    if abs(curr - prev) > 20:
        return jsonify({"alert": "Sudden network drop detected"})
    return jsonify({"alert": "Stable network"})

# ---------- RUN ----------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)