from fyers_apiv3 import fyersModel
from dotenv import load_dotenv
import os
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")

fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="logs")

valid_resolutions = {
    "D", "1D", "5S", "10S", "15S", "30S", "45S",
    "1", "2", "3", "5", "10", "15", "20", "30", "60", "120", "240"
}

date_str = input("Enter the date (YYYY-MM-DD): ").strip()
resolution = input("Enter the resolution: ").strip().upper()

if resolution not in valid_resolutions:
    print("Invalid resolution! Please enter a valid resolution.")
    exit(1)

data = {
    "symbol": "NSE:NIFTY50-INDEX",
    "resolution": resolution,
    "date_format": "1",
    "range_from": date_str,
    "range_to": date_str,
    "cont_flag": "1"
}

response = fyers.history(data=data)

output_file = f"historical-data/data/nifty_data_{date_str}_{resolution}.json"
with open(output_file, "w") as f:
    json.dump(response, f, indent=4)

print(f"Data saved to {output_file}")
