# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 15:01:02 2023


"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import squarify

orders = pd.read_excel('...\Dataset.xlsx')
returned = pd.read_excel('...\Dataset.xlsx', 4)
orders = orders[~orders['Order ID'].isin(returned['Order ID'])]

frequency = orders.groupby('Customer ID')['Order ID'].nunique()
frequency = frequency.to_frame(name = 'Frequency')
frequency['F score'] = pd.qcut(frequency['Frequency'],5, labels = False)
frequency['F score'] = frequency['F score'] + 1

monetary = orders.groupby('Customer ID')['Sales'].sum()
monetary = monetary.to_frame(name = 'Monetary')
monetary['M score'] = pd.qcut(monetary['Monetary'],5, labels = False)
monetary['M score'] = monetary['M score'] + 1

end_date = pd.Timestamp(2017, 12, 31)
recent = orders.groupby('Customer ID').apply(lambda x: (end_date - x['Order Date']).min())
recent = recent.to_frame(name = 'Recent')
recent['R score'] = pd.qcut(recent['Recent'],5, labels = False)
recent['R score'] = recent['R score'] + 1 - 6
print(recent['R score'])

recent['R score'] = recent['R score'].abs()
print(recent['R score'])
RFM = pd.merge(pd.merge(frequency, monetary, on = 'Customer ID'), recent, on = 'Customer ID')
RFM = RFM.loc[:, ['R score','F score','M score']]
RFM['RFM score'] = RFM['R score'].astype(str) + RFM['F score'].astype(str) + RFM['M score']\
.astype(str)

segmentation = pd.read_excel('E:\\Final_project_RFM\Dataset.xlsx', 5)
segmentation['RFM Score'] = segmentation['RFM Score'].apply(lambda x: x.split(','))\
.apply(lambda x: [i.strip() for i in x])

df_temp1 = []
a = 0
for segment in segmentation['Segment']:
    df = RFM[RFM['RFM score'].isin(segmentation.loc[a,'RFM Score'])]
    df['Segment'] = segment
    df_temp1.append(df)
    a = a + 1

RFM_segmented = pd.concat(df_temp1)

RFM_segmented['RFM score'] = RFM_segmented['RFM score'].astype(int)


#Treemap RFM
RFM_count = RFM_segmented.groupby('Segment')['RFM score'].count().to_frame(name = 'Count')
RFM_count['Segment'] = RFM_count.index
RFM_count = RFM_count.sort_values(by= 'Count', ascending=False)
total_customer = RFM_count['Count'].sum()
RFM_count['Value'] = RFM_count['Count']/total_customer*100
RFM_count['Value'] = RFM_count['Value'].round(2)
RFM_count['Label'] = RFM_count['Segment'] + ' \n ' + (RFM_count['Value']).astype(str) + '%'
squarify.plot(sizes=RFM_count['Count'], label=RFM_count['Label'], alpha=0.8,\
text_kwargs = {'fontsize': 8, 'color': 'black'},norm_y = 130,\
color = sns.color_palette("mako", len(RFM_count['Segment'])))
plt.axis('off')
plt.title('RFM Segments of Customer Count (By %)')
plt.show()

#Bar chart
bar_plot = sns.barplot(data = RFM_count, x = 'Segment', y = 'Count')
bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=40, ha="right")
plt.title('RFM Segments of Customer Count')
plt.show()

#Recommendations:
## The goal is to increase customer loyalty and retention, then the Recency score may be the most important. Customers who have made a purchase recently are more likely to make another purchase in the near future, so businesses may want to focus on retaining these customers by offering personalized promotions and incentives.
## The goal is to maximize revenue, then the Monetary score may be the most important because it indicates how much a customer has spent on purchases. Businesses may want to focus their marketing efforts on customers who have spent more money in the past, as they are more likely to make future purchases and generate more revenue.








