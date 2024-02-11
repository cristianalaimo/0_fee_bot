import pandas as pd
import numpy as np
# List of threshold values
thresholds = [50]
dist = 5
# List of n_rows_before 
n_rows_before_values = [3]
# List of bid_ask_ratio_condition values
bid_ask_ratio_values = [5/4]
# List of magnitude values
magnitude_values = [80]
  # Add the magnitudes you want to test
stop_loss=0.9
avg_size=100

min_dist_to_avg=0  #how much the price has to be lower than avg
# List of file paths
file_paths = [#'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_29_01_evening.xlsx',
             #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_30_01_day.xlsx',
             # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_30_01_night.xlsx',
            #   'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_01_02_day.xlsx',
           #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_02_02_day.xlsx',
            #    'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_02_02_night.xlsx',
              #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_03_02_day.xlsx',
             # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_03_02_night.xlsx',
              # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_04_02_day.xlsx',
             # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_04_02_night.xlsx',
           # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_05_02_day.xlsx',
            #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_05_02_night.xlsx',
             #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_06_02_day.xlsx',
              # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_06_02_night.xlsx',
               #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_07_02_day.xlsx',
               #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_07_02_night.xlsx',
               #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_08_02_day.xlsx',
              #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_day.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_night.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_10_02_day.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_10_02_night.xlsx'
                ]

# Loop over file paths
#inizialize the total len plus and total len minus 
# Add new columns for averages


total_len_plus_indices=total_len_minus_indices=0
for excel_path in file_paths:
    df = pd.read_excel(excel_path)
    # Add new columns for averages
    df['avg_100_last_price'] =round( df['Price'].rolling(window=avg_size, min_periods=1).mean(),2)
    df['ratio_range_4'] =round( df['total_bid_volume_in_range_4'] / df['total_ask_volume_in_range_4'],2)
    df['avg_100_last_ratio_range_4']=round(df['ratio_range_4'].rolling(window=avg_size, min_periods=1).mean(),2)
    # Loop over threshold values
    df['size_bid_ask_range_4'] = df['total_bid_volume_in_range_4'].astype(float) + df['total_ask_volume_in_range_4'].astype(float)
    df['avg_size_bid_ask_range_4']=round(df['size_bid_ask_range_4'].rolling(window=avg_size, min_periods=1).mean(),2)
    print('calcoalto')
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
                            # if df.at[n - i, 'ratio_range_4'] < bid_ask_ratio_condition * df.at[n - i, 'avg_100_last_ratio_range_4']:
                           #    break
                            if df.at[n - i, 'total_bid_volume_in_range_4'] < bid_ask_ratio_condition * df.at[n - i, 'total_ask_volume_in_range_4']:
                                 break
                            if not pd.Series(df.at[n - i, 'Price']).between(df.at[n, 'Price'] - dist, df.at[n, 'Price'] + dist).any():
                                break
                            ###controllo open order
                            ##controllo sull'entità del bid assoluta
                            if df.at[n - i, 'total_bid_volume_in_range_4']+df.at[n - i, 'total_ask_volume_in_range_4'] < magnitude_value:
                                break
                           # if df.at[n-i,'size_bid_ask_range_4']<(1)*df.at[n-i,'avg_size_bid_ask_range_4']:
                               # break
                            i += 1
                        if i == n_rows_before:
                            if df.at[n,'Price']+min_dist_to_avg<df.at[n,'avg_100_last_price']:
                                df.at[n, 'label'] = 1

                    # Lists to store indices for +threshold and -threshold
                    plus_indices = []
                    minus_indices = []

                    # Check for target reached based on labeled rows
                    for i in range(len(df)):
                        if df.at[i,'label']==1:
                            #print (df.iloc[i])
                            # Check if the price reaches +threshold or -threshold in the subsequent rows
                            for j in range(1, len(df)-i-1):
                                if df['Price'].iloc[i + j] >= df['Price'].iloc[i] + (threshold):
                                    plus_indices.append(i) 
                                    break
                                elif df['Price'].iloc[i + j] <= df['Price'].iloc[i] - (stop_loss*threshold):
                                    minus_indices.append(i)
                                    break
                                else:df.at[i+j,'label']=0

                    #Print the lists of indices
                    print(f'File: {excel_path}, Threshold: {threshold}, Ratio Check: {bid_ask_ratio_condition}, n_rows_before: {n_rows_before}, Magnitude: {magnitude_value}')
                    print("Indices for +{}:".format(threshold), plus_indices,"Indices for -{}:".format(threshold), minus_indices)
                    len_plus_indices = len(plus_indices)
                    len_minus_indices = len(minus_indices)
                    total_len_plus_indices+=len_plus_indices
                    total_len_minus_indices+=len_minus_indices
                    print("Length of +{} indices:".format(threshold), len_plus_indices, "Length of -{} indices:".format(threshold), len_minus_indices)
                
                    # Print the ratio between the lengths
                    
                    if len_minus_indices != 0:
                        ratio_plus_minus = len_plus_indices / len_minus_indices
                        print("Ratio (len_plus / len_minus):", ratio_plus_minus)
                    else:
                        print("Ratio (len_plus / len_minus): N/A (denominator is zero), len_plus_indices: ",len_plus_indices)
                    
print(f'File: {excel_path}, Threshold: {threshold}, Ratio Check: {bid_ask_ratio_condition}, n_rows_before: {n_rows_before}, Magnitude: {magnitude_value}')
print('avg_size: ',avg_size)                             
print('total len plus indices: ', total_len_plus_indices)
print('total len minus indices: ', total_len_minus_indices)