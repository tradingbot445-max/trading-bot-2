print("🚀 Trading Bot Test Started!")
print("=" * 40)

import os
import requests

# Test environment variables
print("🔍 Checking environment variables...")
print(f"CRYPTOPANIC: {'✅ FOUND' if os.getenv('CRYPTOPANITOKEN') else '❌ MISSING'}")
print(f"EMAIL PASS: {'✅ FOUND' if os.getenv('EMAILPASSWORD') else '❌ MISSING'}")

# Test Binance API
print("\n📈 Testing Binance API...")
try:
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    data = response.json()
    print(f"💰 BTC Price: ${float(data['price']):.2f}")
    print("✅ Binance API: WORKING")
except Exception as e:
    print(f"❌ Binance API Error: {e}")

print("\n🎉 Basic test completed!")
