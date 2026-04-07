from flask import Flask, request, jsonify
import pandas as pd
from model import load_model
import os

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
app = Flask(__name__)

df = pd.read_csv("data.csv")
model = load_model()

# Home
@app.route('/')
def home():
    return "API running"

# Get data
@app.route('/data')
def get_data():
    return df.to_json(orient='records')

# Predict NQS
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    input_data = [[
        data['signal_strength'],
        data['latency'],
        data['speed']
    ]]

    prediction = model.predict(input_data)[0]

    return jsonify({
        "predicted_NQS": round(prediction, 2)
    })

# Recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    suggestions = []

    if data['signal_strength'] < -85:
        suggestions.append("Move to open area")

    if data['latency'] > 100:
        suggestions.append("Avoid peak hours")

    if data['speed'] < 10:
        suggestions.append("Switch network")

    return jsonify({
        "recommendations": suggestions
    })

if __name__ == '__main__':
    