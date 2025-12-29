import requests
import pandas as pd
from datetime import datetime
import json

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Fetching crypto data...")
    
    # Get data
    url = "https://api.coingecko.com/api/v3/search/trending"
    response = requests.get(url)
    data = response.json()
    
    # Process data WITH TRENDING RANK
    coins_data = []
    for index, coin_item in enumerate(data.get('coins', [])):
        coin = coin_item['item']
        coin_info = coin.get('data', {})
        
        coins_data.append({
            'trending_rank': index + 1,  # ADD THIS: 1st, 2nd, 3rd in trending
            'name': coin.get('name', ''),
            'symbol': coin.get('symbol', ''),
            'price': coin_info.get('price', 0),
            'market_cap': str(coin_info.get('market_cap', '')).replace('$', '').replace(',', ''),
            'market_cap_rank': coin.get('market_cap_rank', 0),  # Keep this for reference
            '24h_change': coin_info.get('price_change_percentage_24h', {}).get('usd', 0),
            'timestamp': datetime.now().isoformat()
        })
    
    # Save data
    with open('crypto_data.json', 'w') as f:
        json.dump(coins_data, f, indent=2)
    
    # Also save as CSV
    df = pd.DataFrame(coins_data)
    df.to_csv('crypto_data.csv', index=False)
    
    print(f"Saved {len(coins_data)} trending coins")

if __name__ == "__main__":
    main()
