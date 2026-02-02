import requests
import json


API_KEY = ''
BASE_URL = 'https://api.marketstack.com/v2/'


def fetch_small_cap_data():
    # 1. Fetching data for the Russell 2000 ETF (IWM)
    # 2. Fetching data for specific individual small-cap symbols (e.g., AADI, SMLR)
    symbols = 'IWM,AADI,SMLR'

    params = {
        'access_key': API_KEY,
        'symbols': symbols,
        'limit': 5  # fetch the last 5 days of data for each
    }

    try:
        # /eod endpoint
        response = requests.get(f"{BASE_URL}eod", params=params)
        response.raise_for_status()

        data = response.json()

        print(f"--- Small Cap Data Experiment ---")
        for item in data.get('data', []):
            print(f"Ticker: {item['symbol']} | Date: {item['date'][:10]}")
            print(f"  Open: {item['open']} | Close: {item['close']} | Volume: {item['volume']}")
            print("-" * 30)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")


def fetch_index_info():
    """Fetches details for a specific small-cap benchmark index using v2 /indexinfo."""
    params = {
        'access_key': API_KEY,
        'index': 'RUT'  # RUT is the ticker for Russell 2000 Index
    }

    try:
        response = requests.get(f"{BASE_URL}indexinfo", params=params)
        if response.status_code == 200:
            index_data = response.json()
            print("\n--- Russell 2000 Index Info ---")
            print(json.dumps(index_data, indent=2))
        else:
            print(f"Index endpoint returned status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    fetch_small_cap_data()
    # fetch_index_info()
