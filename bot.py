import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime

print("=" * 50)
print("🤖 ENHANCED TRADING BOT")
print("=" * 50)

# Configuration
EMAIL_ADDRESS = "tradingbot445@gmail.com"
WATCHLIST = ["BTC-USD", "ETH-USD", "BNB-USD"]
PRIMARY_COIN = "BNB-USD"

# Simple in-memory storage (will move to Google Sheets later)
price_history = {symbol: [] for symbol in WATCHLIST}

def check_environment():
    """Check if all required environment variables are set"""
    print("🔍 Checking environment...")
    
    cryptopanic_token = os.getenv('CRYPTOPANITOKEN')
    email_password = os.getenv('EMAILPASSWORD')
    
    if not cryptopanic_token:
        print("❌ CRYPTOPANITOKEN not found")
        return False
        
    if not email_password:
        print("❌ EMAILPASSWORD not found")
        return False
    
    print("✅ Environment variables: OK")
    return True

def get_crypto_data(symbol):
    """Fetch data from Coinbase API"""
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}/spot"
        response = requests.get(url, timeout=10)
        data = response.json()
        price = float(data['data']['amount'])
        
        # Store in history (will move to Google Sheets)
        price_history[symbol].append({
            'timestamp': datetime.now(),
            'price': price
        })
        # Keep only last 50 prices to manage memory
        if len(price_history[symbol]) > 50:
            price_history[symbol].pop(0)
            
        return price
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        return None

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    if len(prices) < period + 1:
        return 50  # Neutral if not enough data
    
    # Convert to simple list of prices
    price_values = [p['price'] for p in prices] if isinstance(prices[0], dict) else prices
    
    gains = []
    losses = []
    
    for i in range(1, len(price_values)):
        change = price_values[i] - price_values[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    
    if len(gains) < period:
        return 50
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100 if avg_gain > 0 else 50
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def check_news():
    """Check for breaking news"""
    print("📰 Checking news...")
    token = os.getenv('CRYPTOPANITOKEN')
    
    try:
        url = f"https://cryptopanic.com/api/v1/posts/?auth_token={token}&limit=5"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        critical_news = []
        for item in data.get('results', []):
            title = item.get('title', '').lower()
            keywords = ['hack', 'sec', 'regulation', 'crash', 'ban', 'lawsuit', 'investigation', 'fed', 'cpi']
            if any(keyword in title for keyword in keywords):
                critical_news.append(title)
                print(f"⚠️ Critical news: {title[:80]}...")
        
        if critical_news:
            return True
        else:
            print("✅ No breaking news found")
            return False
    except Exception as e:
        print(f"❌ News API error: {e}")
        return False

def analyze_trend(prices):
    """Simple trend analysis"""
    if len(prices) < 5:
        return "NEUTRAL"
    
    price_values = [p['price'] for p in prices] if isinstance(prices[0], dict) else prices
    
    recent_prices = price_values[-5:]
    if recent_prices[-1] > recent_prices[0]:
        return "UPTREND"
    elif recent_prices[-1] < recent_prices[0]:
        return "DOWNTREND"
    else:
        return "SIDEWAYS"

def send_trading_alert(symbol, action, price, rsi, trend, reason):
    """Send enhanced email trading alert"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"🚨 {action} - {symbol} - RSI: {rsi}"
        
        # Enhanced risk management
        if action == "BUY":
            stop_loss = price * 0.97  # 3% stop loss
            take_profit_1 = price * 1.03  # 3% take profit
            take_profit_2 = price * 1.06  # 6% take profit
            position_size = calculate_position_size(price, stop_loss)
        else:  # SELL
            stop_loss = price * 1.03  # 3% stop loss
            take_profit_1 = price * 0.97  # 3% take profit
            take_profit_2 = price * 0.94  # 6% take profit
            position_size = calculate_position_size(price, stop_loss)
        
        body = f"""
🤖 ENHANCED TRADING ALERT

ACTION: {action}
SYMBOL: {symbol}
PRICE: ${price:.2f}

TECHNICALS:
• RSI: {rsi} ({'OVERSOLD' if rsi < 30 else 'OVERBOUGHT' if rsi > 70 else 'NEUTRAL'})
• TREND: {trend}

RISK MANAGEMENT:
• Stop Loss: ${stop_loss:.2f}
• Take Profit 1: ${take_profit_1:.2f}
• Take Profit 2: ${take_profit_2:.2f}
• Position Size: ${position_size:.2f}

REASON: {reason}
TIME: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Execute manually on your preferred exchange.
"""
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, os.getenv('EMAILPASSWORD'))
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Enhanced alert sent for {symbol}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def calculate_position_size(entry_price, stop_loss):
    """Better position sizing"""
    risk_per_trade = 0.02  # 2% of portfolio per trade
    portfolio_value = 1000  # Demo portfolio - will be dynamic later
    
    risk_amount = portfolio_value * risk_per_trade
    price_risk = abs(entry_price - stop_loss)
    
    if price_risk == 0:
        return 0
    
    position_size = risk_amount / (price_risk / entry_price)
    return round(position_size, 2)

def analyze_market():
    """Enhanced analysis with technical indicators"""
    print("📈 Analyzing market with technical indicators...")
    
    # Get current prices and update history
    current_prices = {}
    for symbol in WATCHLIST:
        price = get_crypto_data(symbol)
        if price:
            current_prices[symbol] = price
            print(f"💰 {symbol}: ${price:.2f}")
        time.sleep(1)  # Rate limiting
    
    # Technical analysis
    signals_generated = 0
    
    for symbol, current_price in current_prices.items():
        if len(price_history[symbol]) < 15:  # Need enough data for RSI
            print(f"⏳ {symbol}: Collecting more data for analysis...")
            continue
            
        # Calculate indicators
        rsi = calculate_rsi(price_history[symbol])
        trend = analyze_trend(price_history[symbol])
        
        print(f"📊 {symbol}: RSI={rsi}, Trend={trend}")
        
        # Enhanced trading logic
        if rsi < 30 and trend == "UPTREND":  # Oversold in uptrend
            print(f"🎯 STRONG BUY signal for {symbol} at ${current_price:.2f}")
            reason = f"Oversold (RSI: {rsi}) in uptrend"
            if send_trading_alert(symbol, "BUY", current_price, rsi, trend, reason):
                signals_generated += 1
                
        elif rsi > 70 and trend == "DOWNTREND":  # Overbought in downtrend
            print(f"🎯 STRONG SELL signal for {symbol} at ${current_price:.2f}")
            reason = f"Overbought (RSI: {rsi}) in downtrend"
            if send_trading_alert(symbol, "SELL", current_price, rsi, trend, reason):
                signals_generated += 1
                
        elif symbol == "BNB-USD" and current_price < 600 and rsi < 40:
            print(f"🎯 BUY signal for {symbol} at ${current_price:.2f}")
            reason = f"Price below $600 with RSI: {rsi}"
            if send_trading_alert(symbol, "BUY", current_price, rsi, trend, reason):
                signals_generated += 1
    
    return signals_generated

def generate_report():
    """Generate performance report"""
    print("\n📊 GENERATING PERFORMANCE REPORT...")
    
    report = "📈 TRADING BOT REPORT\n"
    report += "=" * 30 + "\n"
    
    for symbol in WATCHLIST:
        if price_history[symbol]:
            current_price = price_history[symbol][-1]['price']
            rsi = calculate_rsi(price_history[symbol]) if len(price_history[symbol]) >= 15 else "N/A"
            trend = analyze_trend(price_history[symbol])
            
            report += f"{symbol}:\n"
            report += f"  Price: ${current_price:.2f}\n"
            report += f"  RSI: {rsi}\n"
            report += f"  Trend: {trend}\n"
            report += f"  Data Points: {len(price_history[symbol])}\n\n"
    
    report += f"⏰ Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(report)
    
    return report

def main():
    """Main function"""
    print("🚀 Starting enhanced trading analysis...")
    
    # Step 1: Check environment
    if not check_environment():
        print("❌ Cannot start - missing credentials")
        return
    
    # Step 2: Check news
    if check_news():
        print("⚠️ Breaking news detected - no trading")
        return
    
    # Step 3: Enhanced market analysis
    signals = analyze_market()
    
    # Step 4: Generate report
    generate_report()
    
    print(f"\n✅ Enhanced analysis complete! {signals} trading signals generated.")
    print(f"📈 Next step: Connect to Google Sheets for permanent data storage!")

if __name__ == "__main__":
    main()
