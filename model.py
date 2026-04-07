import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

def train_model():
    df = pd.read_csv("data.csv")

    # NQS calculation
    df['signal_norm'] = df['signal_strength'] + 100
    df['latency_norm'] = 100 - df['latency']
    df['speed_norm'] = df['speed'] * 2

    df['NQS'] = (
        df['signal_norm'] +
        df['latency_norm'] +
        df['speed_norm']
    ) / 3

    X = df[['signal_strength', 'latency', 'speed']]
    y = df['NQS']

    model = LinearRegression()
    model.fit(X, y)

    # Save model
    pickle.dump(model, open("model.pkl", "wb"))
    print("✅ model.pkl created")

def load_model():
    return pickle.load(open("model.pkl", "rb"))