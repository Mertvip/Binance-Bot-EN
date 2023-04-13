import json
from binance.client import Client

# Load APİ Key
with open('api_keys.json', 'r') as f:
    api_keys = json.load(f)

# Connect with Binance API
client = Client(api_keys['binance_api_key'], api_keys['binance_api_secret'])

# Set coins and strategy
coin = 'ETHBTC'
strategy = 'ema'

# Set parameters for EMA strategy
if strategy == 'ema':
    interval = '1h'
    ema_short_period = 20
    ema_long_period = 50

# Trade according to strategy in endless loop
while True:
    # Calculate the final price of the strategy to use
    if strategy == 'ema':
        klines = client.get_historical_klines(coin, interval, '1 day ago UTC')
        close_prices = [float(kline[4]) for kline in klines]
        ema_short = sum(close_prices[-ema_short_period:]) / ema_short_period
        ema_long = sum(close_prices[-ema_long_period:]) / ema_long_period
        last_price = float(client.get_symbol_ticker(symbol=coin)['price'])
        if last_price > ema_long and last_price > ema_short:
            # Buy
            quantity = 0.1 # Sample quantity, adjust by yourself
            buy_price = 0.05000000 # The price you want to buy
            buy_order = client.create_order(
                symbol=coin,
                side='BUY',
                type='LIMIT',
                timeInForce='GTC', # hold permanently
                price=buy_price,
                quantity=quantity
            )
            print(f'Bought {quantity} {coin} at {buy_price}')
        elif last_price < ema_long and last_price < ema_short:
            # Sell
            sell_price = 0.05500000 # the price you want to sell
            sell_order = client.create_order(
                symbol=coin,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC', # hold permanently
                price=sell_price,
                quantity=quantity
            )
            print(f'Sold {quantity} {coin} at {sell_price}')
    
    # a certain time
