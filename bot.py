print("🚀 Trading Bot Test Started!")
print("=" * 40)

import os
import requests

# Test 1: Check environment variables
print("🔍 Checking environment variables...")
print(f"CRYPTOPANIC: {'✅ FOUND' if os.getenv('CRYPTOPANITOKEN') else '❌ MISSING'}")
print(f"EMAIL PASS: {'✅ FOUND' if os.getenv('EMAILPASSWORD') else '❌ MISSING'}")

# Test 2: Check Binance API (fixed version)
print("\n📈 Testing Binance API...")
try:
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    print(f"💰 BTC Price: ${float(data['price']):.2f}")
    print("✅ Binance API: WORKING")
except Exception as e:
    print(f"❌ Binance API Error: {e}")

# Test 3: Check CryptoPanic News API
print("\n📰 Testing News API...")
try:
    token = os.getenv('CRYPTOPANITOKEN')
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ News API: WORKING")
    else:
        print(f"❌ News API Status: {response.status_code}")
except Exception as e:
    print(f"❌ News API Error: {e}")

print("\n🎉 All tests completed!")
