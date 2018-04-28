# -*- coding:utf-8 -*-
#V:Python 3.6.3
import pandas as pd
from IPython.display import display
from matplotlib.pylab import plt

data = pd.read_csv('house3.csv')
data['total_price'] = data['price']*data['area']/10000

data_mean = data.groupby('district')['price'].mean()
data_count = data.groupby('district')['price'].count()

#柱状图分析各区的二手房的房价
plt.figure(figsize=(10,6))
plt.rc('font',family='SimHei',size=13)
plt.title(u'各区域的平均二手房房价')
plt.xlabel(u'南京城区')
plt.ylabel(u'平均房价')
plt.bar(data_mean.index,data_count.values,color='g')
plt.show()

plt.figure(figsize=(10,10))
plt.rc('font',family='SimHei',size=13)
explode = [0]*len(data_count)
explode[9] = 0.1
plt.pie(data_count,radius=2,autopct='%1.f%%',shadow=True,labels=data_mean.index,explode=explode)
plt.axis('equal')
plt.show()

