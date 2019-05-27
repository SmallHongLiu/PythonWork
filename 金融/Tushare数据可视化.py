# coding=utf-8
'''
Author: Small_Hong
date: 2019-05-27 15:46
'''

import tushare as ts
import matplotlib.pyplot as plt
from datetime import datetime

"""
data = ts.get_hist_data('600848', start='2018-03-01', end='2018-03-31')
# 对交易时间进行降序排列
data = data.sort_index()

xs = [datetime.strptime(d, '%Y-%m-%d').toordinal() for d in data.index]
plt.plot_date(xs, data['open'], 'b-')
plt.gcf().autofmt_xdate()  # 自动旋转日期标记
plt.show()
"""

import matplotlib.dates as mdates

data = ts.get_hist_data('600848', ktype='60')
xs = [mdates.strpdate2num('%Y-%m-%d %H:%M:%S')(d) for d in data.index]

#设置时间标签显示格式
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

plt.plot_date(xs, data['open'], '-', label='open')
plt.legend(loc=0)

plt.gcf().autofmt_xdate()
plt.show()



