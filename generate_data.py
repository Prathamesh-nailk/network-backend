import pandas as pd
import numpy as np

np.random.seed(42)

cities = ["Mumbai","Pune","Delhi","Bangalore","Hyderabad","Chennai","Kolkata","Ahmedabad","Jaipur","Lucknow"]

rows = []

for i in range(1000):
    city = np.random.choice(cities)
    location = f"{city}_{np.random.randint(1,10)}"
    
    signal_strength = np.random.randint(-95, -60)
    latency = np.random.randint(20, 150)
    speed = np.random.randint(5, 40)
    time = np.random.randint(0, 24)
    
    rows.append([location, signal_strength, latency, speed, time])

df = pd.DataFrame(rows, columns=[
    "location","signal_strength","latency","speed","time"
])

df.to_csv("data.csv", index=False)

print("✅ data.csv created")