import requests


API_KEY = ''
BASE_URL = 'https://api.twelvedata.com'


def check_api_health():
    url = f"{BASE_URL}/api_usage"
    params = {'apikey': API_KEY}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            print("--- API Health Check: SUCCESS ---")
            print(f"Plan: {data.get('plan_name')}")
            print(f"Credits Used Today: {data.get('timestamp_usage', 0)}")
            return True
        else:
            print(f"--- API Health Check: FAILED ({response.status_code}) ---")
            print(data.get('message'))
            return False
    except Exception as e:
        print(f"Error connecting to Twelve Data: {e}")
        return False


def get_small_cap_data(symbol):
    url = f"{BASE_URL}/quote"
    params = {
        'symbol': symbol,
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'code' in data and data['code'] != 200:
        print(f"Error fetching {symbol}: {data['message']}")
        return

    print(f"\n--- Data Snapshot: {symbol} ---")
    print(f"Name: {data.get('name')}")
    print(f"Exchange: {data.get('exchange')}")
    print(f"Current Price: {data.get('price')} {data.get('currency')}")
    print(f"Day Change: {data.get('change')} ({data.get('percent_change')}%)")
    print(f"52-Week High: {data.get('fifty_two_week', {}).get('high')}")


def get_historical_intraday(symbol):
    url = f"{BASE_URL}/time_series"
    params = {
        'symbol': symbol,
        'interval': '1min',
        'outputsize': 5,
        'apikey': API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get('status') == 'ok':
        print(f"\n--- Recent 1-Min Intervals for {symbol} ---")
        for bar in data.get('values', []):
            print(f"Time: {bar['datetime']} | Close: {bar['close']} | Vol: {bar['volume']}")
    else:
        print(f"Could not fetch time series: {data.get('message')}")


if __name__ == "__main__":
    if check_api_health():
        get_small_cap_data('IWM')
        get_historical_intraday('SMLR')