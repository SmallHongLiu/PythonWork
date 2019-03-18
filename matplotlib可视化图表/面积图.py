import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
通过对轴和线之间的区域进行着色，面积图不仅强调峰和谷，而且还强调高点和低点的持续时间。 高点持续时间越长，线下面积越大
'''

df = pd.read_csv("https://github.com/selva86/datasets/raw/master/economics.csv", parse_dates=['date']).head(100)
x = np.arange(df.shape[0])
y_returns = (df.psavert.diff().fillna(0) / df.psavert.shift(1)).fillna(0)* 100

plt.figure(figsize=(16, 10), dpi=80)
plt.fill_between(x[1:], y_returns[1:], 0, where = y_returns[1:] >= 0, facecolor='green')
plt.fill_between(x[1:], y_returns[1:], 0, where = y_returns[1:] <= 0, facecolor='red')

plt.annotate('Peak \n1975', xy=(47.0, 13.5), xytext=(88.0, 28),
             bbox=dict(boxstyle='square', fc='firebrick'),
             arrowprops=dict(facecolor='steelblue', shrink=0.05), fontsize=15, color='white')

xtickvals = [str(m)[:3].upper() + '-' + str(y) for y, m in zip(df.date.dt.year, df.date.dt.month_name())]
plt.gca().set_xticks(x[::6])
plt.gca().set_xticklabels(xtickvals[::6], rotation=90, fontdict={'horizontalalignment': 'center', 'verticalalignment': 'center_baseline'})
plt.ylim(-35, 35)
plt.xlim(1, 100)
plt.title("Month Economics Return %", fontsize=22)
plt.ylabel('Monthly returns %')
plt.grid(alpha=0.5)
plt.show()
