print("🚀 Trading Bot Test - Coinbase Version")
print("=" * 40)

import os
import requests

# Test 1: Check environment variables
print("🔍 Checking environment variables...")
print(f"CRYPTOPANIC: {'✅ FOUND' if os.getenv('CRYPTOPANITOKEN') else '❌ MISSING'}")
print(f"EMAIL PASS: {'✅ FOUND' if os.getenv('EMAILPASSWORD') else '❌ MISSING'}")

# Test 2: Use Coinbase API instead of Binance
print("\n📈 Testing Crypto API (Coinbase)...")
try:
    url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        btc_price = float(data['data']['amount'])
        print(f"💰 BTC Price: ${btc_price:.2f}")
        print("✅ Crypto API: WORKING")
    else:
        print(f"❌ Crypto API Status: {response.status_code}")
except Exception as e:
    print(f"❌ Crypto API Error: {e}")

# Test 3: Check multiple coins
print("\n💰 Getting multiple coin prices...")
coins = {
    'BTC': 'BTC-USD',
    'ETH': 'ETH-USD', 
    'BNB': 'BNB-USD'
}

for coin, pair in coins.items():
    try:
        url = f"https://api.coinbase.com/v2/prices/{pair}/spot"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = float(data['data']['amount'])
            print(f"   {coin}: ${price:.2f}")
        else:
            print(f"   {coin}: ❌ API Error")
    except Exception as e:
        print(f"   {coin}: ❌ Error")

# Test 4: Check CryptoPanic News API
print("\n📰 Testing News API...")
try:
    token = os.getenv('CRYPTOPANITOKEN')
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&limit=1"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        print("✅ News API: WORKING")
    else:
        print(f"❌ News API Status: {response.status_code}")
except Exception as e:
    print(f"❌ News API Error: {e}")

print("\n🎉 All tests completed!")
