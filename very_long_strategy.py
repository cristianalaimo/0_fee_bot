import pandas as pd
import numpy as np

dist = 5
# List of n_rows_before 
n_rows_before_values = [1]
# List of bid_ask_ratio_condition values
bid_ask_ratio_values = [5/4]
# List of magnitude values
magnitude_values = [90]
  # Add the magnitudes you want to test
stop_loss=0.95
avg_size_lists=[100]
threshold=100
tot_plus=tot_minus=0

total_len_plus_indices=total_len_minus_indices=0

min_dist_to_avg=-100 #how much the price has to be lower than avg
# List of file paths
file_paths = [#'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_29_01_evening.xlsx',
            # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_30_01_day.xlsx',
              #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_30_01_night.xlsx',
             #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_01_02_day.xlsx',
            #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_02_02_day.xlsx',
              #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_02_02_night.xlsx',
             #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_03_02_day.xlsx',
            #   'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_03_02_night.xlsx',
           #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_04_02_day.xlsx',
             # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_04_02_night.xlsx',
            # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_05_02_day.xlsx',
           #  'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_05_02_night.xlsx',
              #'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_06_02_day.xlsx',
             # 'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_06_02_night.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_07_02_day.xlsx',
              'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_07_02_night.xlsx',
              'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_08_02_day.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_day.xlsx',
               'C:/Users/c.alaimo/Desktop/python/progettino/gpt/order_book_data_09_02_night.xlsx'
                ]

for excel_path in file_paths:
    print(excel_path)
    df = pd.read_excel(excel_path) 
    df['label'] = 0
    for avg_size in avg_size_lists:
        # Add new columns for averages
        df['avg_100_last_price'] =round( df['Price'].rolling(window=avg_size, min_periods=1).mean(),2)
        df['avg_100_last_price_2'] =round( df['Price'].rolling(window=20, min_periods=1).mean(),2)
        for n_rows_before in n_rows_before_values:
            plus_indices=[]
            minus_indices=[]
            # Loop over bid_ask_ratio_condition values
            n=101
            while n<len(df):
                                if df.at[n,'Price']+min_dist_to_avg<df.at[n,'avg_100_last_price'] and not  df.at[n,'Price']+min_dist_to_avg/2<df.at[n,'avg_100_last_price_2']:
                                    df.at[n, 'label'] = 1
                                    print(n)
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
            
            print(plus_indices,len(plus_indices))
            
            print(minus_indices,len(minus_indices))
            tot_plus+=len(plus_indices)
            tot_minus+=len(minus_indices)


print(tot_plus,tot_minus)