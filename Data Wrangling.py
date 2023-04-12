# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 14:51:36 2023

@author: ASUS
"""

import pandas as pd



sales_table = pd.read_csv('E:\Data Wrangling Practise\Data Wrangling Practise\sales.csv',skipinitialspace = True)
prices_table = pd.read_csv('E:\Data Wrangling Practise\Data Wrangling Practise\prices.csv',skipinitialspace = True)
sales_table['ordered_at'] = pd.to_datetime(sales_table['ordered_at'], format='%m/%d/%y %H:%M')
prices_table['updated_at'] = pd.to_datetime(prices_table['updated_at'], format='%m/%d/%y %H:%M')

df1 = sales_table.sort_values(by = ['product_id','ordered_at'])
df2 = prices_table.sort_values(by = ['product_id','updated_at'])
#df4 = pd.merge_asof(df1, df2, left_on = 'ordered_at', right_on = 'updated_at',by='product_id', direction='forward')
#print(df4)

df2['start_date'] = df2.groupby('product_id')['updated_at'].shift(1,fill_value = pd.Timestamp('2018-01-01'))


df2 = df2.loc[:, ['product_id','old_price','start_date' ,'updated_at']]
df2 = df2.rename(columns = {'updated_at':'end_date','old_price':'price'})

df3 = prices_table.loc[prices_table.groupby('product_id')['updated_at'].idxmax()]
df3 = df3.loc[:, ['product_id','new_price','updated_at']]
df3 = df3.rename(columns = {'updated_at':'start_date','new_price':'price'})
df3['end_date'] = pd.Timestamp('2018-12-31 23:59:59')
print(df3)
df2 = pd.concat([df2,df3])
df2 = df2.sort_values(by = 'end_date')
df1 = df1.sort_values(by = 'ordered_at')
df4 = pd.merge_asof(df1, df2, left_on = 'ordered_at', right_on = 'end_date',by='product_id' ,direction='forward')

df4['revenue'] = df4['price']*df4['quantity_ordered']
df4 = df4.groupby(['product_id','price'])['revenue'].sum()
print(df4)