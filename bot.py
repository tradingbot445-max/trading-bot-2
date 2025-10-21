print("🚀 Trading Bot Test - Simple Version")
print("=" * 40)

import os
import requests

# Test 1: Check environment variables
print("🔍 Checking environment variables...")
print(f"CRYPTOPANIC: {'✅ FOUND' if os.getenv('CRYPTOPANITOKEN') else '❌ MISSING'}")
print(f"EMAIL PASS: {'✅ FOUND' if os.getenv('EMAILPASSWORD') else '❌ MISSING'}")

# Test 2: Simple Binance API test
print("\n📈 Testing Binance API...")
try:
    # Use the most basic endpoint
    url = "https://api.binance.com/api/v3/ping"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        print("✅ Binance API Connection: WORKING")
    else:
        print(f"❌ Binance API Status: {response.status_code}")
except Exception as e:
    print(f"❌ Binance API Error: {e}")

# Test 3: Get actual price (simplified)
print("\n💰 Getting BTC Price...")
try:
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print(f"BTC Price Response: {data}")
        if 'price' in data:
            print(f"✅ BTC Price: ${float(data['price']):.2f}")
        else:
            print(f"❌ Price key missing: {data}")
    else:
        print(f"❌ Price API Status: {response.status_code}")
except Exception as e:
    print(f"❌ Price API Error: {e}")

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
