import json
import pandas as pd
import plotly.graph_objects as go
import os

file_path = input("Enter the JSON filename: ").strip()

if not os.path.isfile(file_path):
    print("File not found.")
    exit(1)

with open(file_path, "r") as f:
    data = json.load(f)

if not data.get("candles"):
    print("No candle data found in the file.")
    exit(1)

df = pd.DataFrame(data["candles"], columns=["time", "open", "high", "low", "close", "volume"])
df["time"] = pd.to_datetime(df["time"], unit="s", utc=True).dt.tz_convert("Asia/Kolkata")

fig = go.Figure(data=[go.Candlestick(
    x=df["time"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="Candles"
)])

fig.update_layout(
    title="",
    xaxis_title="",
    yaxis_title="",
    xaxis_rangeslider_visible=True,
    template="plotly_dark",
    dragmode="pan",
    yaxis=dict(
        tickformat=",",
        separatethousands=True,
        side="right",
        fixedrange=False
    ),
    xaxis=dict(
        fixedrange=False
    ),
)

fig.show()
