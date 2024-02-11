import os
print("Current Working Directory:", os.getcwd())
import requests
from datetime import datetime
import time
import pandas as pd

import numpy as np

def get_order_book_snapshot(market, limit):
    base_url = 'https://api.binance.com/api/v3/depth'
    params = {
        'symbol': market,
        'limit': limit
    }
    response = requests.get(base_url, params=params)
    return response.json()

def create_instance(order_book_data):
    instance = {'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}
    bids = order_book_data['bids']
    asks = order_book_data['asks']

    for i, bid in enumerate(bids):
        instance[f'Bid_Price_{i+1}'] = float(bid[0])  # Convert to float
        instance[f'Bid_Quantity_{i+1}'] = float(bid[1])  # Convert to float

    for i, ask in enumerate(asks):
        instance[f'Ask_Price_{i+1}'] = float(ask[0])  # Convert to float
        instance[f'Ask_Quantity_{i+1}'] = float(ask[1])  # Convert to float

    return instance
#
def calculate_rsi(prices, window):
    close_prices = np.diff(prices)
    gain = np.where(close_prices > 0, close_prices, 0)
    loss = -np.where(close_prices < 0, close_prices, 0)
    avg_gain = np.convolve(gain, np.ones(window)/window, mode='valid')
    avg_loss = np.convolve(loss, np.ones(window)/window, mode='valid')
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi



# Set the trading pair and limit
market = 'BTCFDUSD'
limit = 1000 # Number of orders to fetch on each side of the order book
rsi_len=10
rsi_prices=[]
order_book_snapshot = get_order_book_snapshot(market, limit)
instance = create_instance(order_book_snapshot)

# we want to fetch data about total bid and ask volume for the last n minutes [referred as duration_minutes]:
duration_minutes = 600
end_time = time.time() + duration_minutes * 60
total_bid_volume_last_minutes = 0
total_ask_volume_last_minutes = 0

furthest_bid_price = None
furthest_ask_price = None

#Choose the range where we want to calculate the sum of volumes (price offer not further than actual price +- range)
price_range_1=5
price_range_2=10
price_range_3=20
price_range_4=50
price_range_5=100
# Create an empty list to store the data
data = []
while time.time() < end_time:
    try:
        order_book_snapshot = get_order_book_snapshot(market, limit)
        
        best_bid_price,best_ask_price = float(order_book_snapshot['bids'][0][0]), float(order_book_snapshot['asks'][0][0])
        price=(best_ask_price+best_bid_price)/2
        total_bid_volume, total_ask_volume = round(sum(float(bid[1]) for bid in order_book_snapshot['bids']), 2), round(sum(float(ask[1]) for ask in order_book_snapshot['asks']), 2)
        ratio_bid_ask_100orders=round(total_bid_volume/total_ask_volume,2)

        total_bid_volume_last_minutes += total_bid_volume
        total_ask_volume_last_minutes += total_ask_volume
        total_bid_volume_last_minutes, total_ask_volume_last_minutes = round(total_bid_volume_last_minutes, 2), round(total_ask_volume_last_minutes, 2)

        furthest_bid_price,furthest_ask_price = float(order_book_snapshot['bids'][-1][0]),float(order_book_snapshot['asks'][-1][0])
        total_bid_volume_in_range_1 = total_ask_volume_in_range_1 = total_bid_volume_in_range_2 = total_ask_volume_in_range_2 = total_bid_volume_in_range_3 = total_ask_volume_in_range_3 = total_bid_volume_in_range_4=total_ask_volume_in_range_4 =total_bid_volume_in_range_5=total_ask_volume_in_range_5=0

        central_price = (best_bid_price + best_ask_price) / 2
        #calculate RSI
        RSI=0
        rsi_prices.append(central_price)
        if len(rsi_prices)>rsi_len:
            RSI=calculate_rsi(rsi_prices, rsi_len)
            rsi_prices.pop(0)


        total_bid_volume_in_range_1 += sum(float(bid[1]) for bid in order_book_snapshot['bids'] if central_price - price_range_1 <= float(bid[0]))
        total_ask_volume_in_range_1 += sum(float(ask[1]) for ask in order_book_snapshot['asks'] if float(ask[0]) <= central_price + price_range_1)
        total_bid_volume_in_range_1=round(total_bid_volume_in_range_1,2)
        total_ask_volume_in_range_1=round(total_ask_volume_in_range_1,2)

        total_bid_volume_in_range_2 += sum(float(bid[1]) for bid in order_book_snapshot['bids'] if central_price - price_range_2 <= float(bid[0]))
        total_ask_volume_in_range_2 += sum(float(ask[1]) for ask in order_book_snapshot['asks'] if float(ask[0]) <= central_price + price_range_2)
        total_bid_volume_in_range_2=round(total_bid_volume_in_range_2,2)
        total_ask_volume_in_range_2=round(total_ask_volume_in_range_2,2)

        total_bid_volume_in_range_3 += sum(float(bid[1]) for bid in order_book_snapshot['bids'] if central_price - price_range_3 <= float(bid[0]))
        total_ask_volume_in_range_3 += sum(float(ask[1]) for ask in order_book_snapshot['asks'] if float(ask[0]) <= central_price + price_range_3)
        total_bid_volume_in_range_3=round(total_bid_volume_in_range_3,2)
        total_ask_volume_in_range_3=round(total_ask_volume_in_range_3,2)

        total_bid_volume_in_range_4 += sum(float(bid[1]) for bid in order_book_snapshot['bids'] if central_price - price_range_4 <= float(bid[0]))
        total_ask_volume_in_range_4 += sum(float(ask[1]) for ask in order_book_snapshot['asks'] if float(ask[0]) <= central_price + price_range_4)
        total_bid_volume_in_range_4=round(total_bid_volume_in_range_4,2)
        total_ask_volume_in_range_4=round(total_ask_volume_in_range_4,2)

        total_bid_volume_in_range_5 += sum(float(bid[1]) for bid in order_book_snapshot['bids'] if central_price - price_range_5 <= float(bid[0]))
        total_ask_volume_in_range_5 += sum(float(ask[1]) for ask in order_book_snapshot['asks'] if float(ask[0]) <= central_price + price_range_5)
        total_bid_volume_in_range_5=round(total_bid_volume_in_range_5,2)
        total_ask_volume_in_range_5=round(total_ask_volume_in_range_5,2)

        print(round(price,2),'   ',ratio_bid_ask_100orders,
            total_bid_volume,
            total_ask_volume,'        RSI_last ',rsi_len,': ', RSI)
        print(
            'distanze bid,ask',
            round(float(order_book_snapshot["bids"][0][0])-(furthest_bid_price),2),
            round((furthest_ask_price)-float(order_book_snapshot["asks"][0][0]),2))
        print(
            'range: 5 - 10 - 20 - 50 - 100    ',
            total_bid_volume_in_range_1,total_ask_volume_in_range_1,'     ',
            total_bid_volume_in_range_2,total_ask_volume_in_range_2, '     ',
            total_bid_volume_in_range_3,total_ask_volume_in_range_3,'     ',
            total_bid_volume_in_range_4,total_ask_volume_in_range_4,'     ',
            total_bid_volume_in_range_5,total_ask_volume_in_range_5)
        print()
        
        data.append({
            'Price': price,
            'ratio bid/ask 100orders':ratio_bid_ask_100orders,
            'total_bid_volume': total_bid_volume,
            'total_ask_volume': total_ask_volume,
            'total_bid_volume_in_range_1': total_bid_volume_in_range_1,
            'total_ask_volume_in_range_1': total_ask_volume_in_range_1,
            'total_bid_volume_in_range_2': total_bid_volume_in_range_2,
            'total_ask_volume_in_range_2': total_ask_volume_in_range_2,
            'total_bid_volume_in_range_3': total_bid_volume_in_range_3,
            'total_ask_volume_in_range_3': total_ask_volume_in_range_3,
            'total_bid_volume_in_range_4': total_bid_volume_in_range_4,
            'total_ask_volume_in_range_4': total_ask_volume_in_range_4,
            'total_bid_volume_in_range_5': total_bid_volume_in_range_5,
            'total_ask_volume_in_range_5': total_ask_volume_in_range_5,
            'bid_vol_acc':total_bid_volume_last_minutes,
            'bid_ask_vol':total_ask_volume_last_minutes,
            f'RSI_{rsi_len}_timeframe': RSI
        })
        time.sleep(2)   
    except Exception as e:
        df = pd.DataFrame(data)
        excel_path = 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_11_02_day.xlsx'
        df.to_excel(excel_path, index=False)


    
# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)
excel_path = 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_11_02_day.xlsx'
df.to_excel(excel_path, index=False)


