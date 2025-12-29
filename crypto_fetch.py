# crypto_fetch.py
import requests
import pandas as pd
from datetime import datetime
import os
import json

def fetch_crypto_data():
    """Fetch trending crypto data from CoinGecko"""
    try:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting data fetch...")
        
        # API call
        url = "https://api.coingecko.com/api/v3/search/trending"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Process data
        coins_data = []
        for coin_item in data.get('coins', []):
            coin = coin_item['item']
            coin_info = coin.get('data', {})
            
            coins_data.append({
                'timestamp': datetime.now().isoformat(),
                'name': coin.get('name', ''),
                'symbol': coin.get('symbol', ''),
                'price': coin_info.get('price', 0),
                'market_cap': str(coin_info.get('market_cap', '')).replace('$', '').replace(',', ''),
                'market_cap_rank': coin.get('market_cap_rank', 0),
                '24h_change': coin_info.get('price_change_percentage_24h', {}).get('usd', 0)
            })
        
        return coins_data
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def save_data(coins_data):
    """Save data to files"""
    if not coins_data:
        print("No data to save")
        return
    
    # Save as JSON
    with open('crypto_data.json', 'w') as f:
        json.dump(coins_data, f, indent=2)
    
    # Save as CSV
    df = pd.DataFrame(coins_data)
    df.to_csv('crypto_data.csv', index=False)
    
    print(f"Saved {len(coins_data)} records")
    print(f"Latest: {coins_data[0]['name']} - ${coins_data[0]['price']:.4f}")

if __name__ == "__main__":
    data = fetch_crypto_data()
    save_data(data)
