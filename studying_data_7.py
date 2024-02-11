import pandas as pd
import numpy as np

# List of threshold values
thresholds = [50]
dist = 5
# List of n_rows_before 
n_rows_before_values = [3,4,5,6]
# List of bid_ask_ratio_condition values
bid_ask_ratio_values = [1,5/4,6/4,7/4]
# List of magnitude values
magnitude_values = [60,70,80]
# Add the magnitudes you want to test
stop_loss = 0.9
avg_size = 100
# List of min_dist_to_avg values
min_dist_to_avg_values = [0]

# List of file paths
file_paths = [
            # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_08_02_day.xlsx',
              # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_day.xlsx',
  #   'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_night.xlsx',
    # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_10_02_day.xlsx',
    'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_10_02_night.xlsx'
]

# Loop over min_dist_to_avg values
for min_dist_to_avg in min_dist_to_avg_values:
    for excel_path in file_paths:
        print(2)
        df = pd.read_excel(excel_path)
        # Add new columns for averages
        df['avg_100_last_price'] = round(df['Price'].rolling(window=avg_size, min_periods=1).mean(), 2)
        # Loop over threshold values
        for threshold in thresholds:
            # Loop over n_rows_before values
            for n_rows_before in n_rows_before_values:
                # Loop over bid_ask_ratio_condition values
                for bid_ask_ratio_condition in bid_ask_ratio_values:
                    # Loop over magnitude values
                    for magnitude_value in magnitude_values:
                        df['label'] = 0
                        for n in range(n_rows_before, len(df)):
                            i = 0
                            while i < n_rows_before:
                                if df.at[n - i, 'total_bid_volume_in_range_4'] < bid_ask_ratio_condition * df.at[n - i, 'total_ask_volume_in_range_4']:
                                    break
                                if not pd.Series(df.at[n - i, 'Price']).between(df.at[n, 'Price'] - dist, df.at[n, 'Price'] + dist).any():
                                    break
                                if df.at[n - i, 'total_bid_volume_in_range_4'] + df.at[n - i, 'total_ask_volume_in_range_4'] < magnitude_value:
                                    break
                                i += 1
                            if i == n_rows_before:
                                if df.at[n, 'Price'] + min_dist_to_avg < df.at[n, 'avg_100_last_price']:
                                    df.at[n, 'label'] = 1
                                    

                        # Lists to store indices for +threshold and -threshold
                        plus_indices = []
                        minus_indices = []

                        # Check for target reached based on labeled rows
                        n=101
                        while n<len(df):
                            if df.at[n, 'label']==1:
                                print (df.at[n,'Price'],min_dist_to_avg,df.at[n,'avg_100_last_price'])
                                for j in range(1, len(df)-n-1):
                                    if df['Price'].iloc[n+ j] >= df['Price'].iloc[n] + (threshold):
                                        plus_indices.append(n) 
                                        break
                                    elif df['Price'].iloc[n + j] <= df['Price'].iloc[n] - (stop_loss*threshold):
                                        minus_indices.append(n)
                                        break
                                    else:df.at[n+j,'label']=0
                                n+=j
                            n+=1
            

                        len_plus_indices = len(plus_indices)
                        len_minus_indices = len(minus_indices)
                        print(f' {excel_path}, {threshold}, {bid_ask_ratio_condition}, {n_rows_before},{magnitude_value},{avg_size},{min_dist_to_avg},{len_plus_indices}, {len_minus_indices }')

print(f' {excel_path}, {threshold}, {bid_ask_ratio_condition}, {n_rows_before},{magnitude_value},{avg_size},{min_dist_to_avg}')
