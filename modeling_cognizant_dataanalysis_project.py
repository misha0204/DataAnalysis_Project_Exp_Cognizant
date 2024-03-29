# -*- coding: utf-8 -*-
"""modeling_Cognizant.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sPMznY6YgEkXnCDswfB1J1yzgLn7oIC-
"""



from google.colab import drive
drive.mount('/content/drive/')
! pip install pandas
import pandas as pd
from datetime import datetime

path = "/content/drive/MyDrive/Colab_Notebooks/"

sales_df = pd.read_csv(f"{path}sample_sales_data.csv")
sales_df.drop(columns= ["unnamed: 0"], inplace = True, errors = 'ignore')
sales_df.head()

def convert_to_datetime(data: pd.DataFrame = None, column: str = None):
    dummy = data.copy()
    dummy[column] = pd.to_datetime(dummy[column], format='%Y-%m-%d %H:%M:%S')
    return dummy

def convert_timestamp_to_hourly(data: pd.DataFrame = None, column: str = None):
  dummy = data.copy()
  new_ts = dummy[column].tolist()
  new_ts = [i.strftime('%Y-%m-%d %H:00:00') for i in new_ts]
  new_ts = [datetime.strptime(i, '%Y-%m-%d %H:00:00') for i in new_ts]
  dummy[column] = new_ts
  return dummy

sales_df = convert_to_datetime(sales_df, 'timestamp')
#sales_df.info()
sales_df.head()
sales_agg = sales_df.groupby(['timestamp', 'product_id']).agg({'quantity':'sum'}).reset_index()
sales_agg.head()

temp_df = pd.read_csv(f"{path}sensor_storage_temperature.csv")
temp_df.drop(columns=["Unnamed: 0"], inplace=True, errors='ignore')
temp_df.head()

temp_df = convert_to_datetime(temp_df, 'timestamp')

temp_df = convert_timestamp_to_hourly(temp_df,'timestamp')
temp_df.head()
stock_agg = stock_df.groupby(['timestamp', 'product_id']).agg({'estimated_stock_pct': 'mean'}).reset_index()
stock_agg.head()
temp_agg = temp_df.groupby(['timestamp']).agg({'temperature': 'mean'}).reset_index()

product_categories = sales_df[['product_id', 'category']]
product_categories = product_categories.drop_duplicates()

product_price = sales_df[['product_id', 'unit_price']]
product_price = product_price.drop_duplicates()

merged_df = stock_agg.merge(sales_agg, on=['timestamp','product_id'], how='left')
merged_df.head()
#merging the data and training the model
merged_df['timestamp_day_of_month'] = merged_df['timestamp'].dt.day
merged_df['timestamp_day_of_week'] = merged_df['timestamp'].dt.dayofweek
merged_df['timestamp_hour'] = merged_df['timestamp'].dt.hour
merged_df.drop(columns=['timestamp'], inplace=True)
merged_df.head()