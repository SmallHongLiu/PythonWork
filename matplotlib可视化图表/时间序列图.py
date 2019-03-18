import pandas as pd
import matplotlib.pyplot as plt

'''
时间序列图用于显示给定度量随时间变化的方式。 在这里，您可以看到 1949年 至 1969年间航空客运量的变化情况。
'''

df = pd.read_csv('https://github.com/selva86/datasets/raw/master/AirPassengers.csv')

plt.figure(figsize=(16, 10), dpi=80)
plt.plot('date', 'value', data=df, color='tab:red')

plt.ylim(50, 750)
xtick_location = df.index.tolist()[::12]
xtick_labels = [x[:4] for x in df.date.tolist()[::12]]
plt.xticks(ticks=xtick_location, labels=xtick_labels, rotation=0, fontsize=12, horizontalalignment='center', alpha=.7)
plt.yticks(fontsize=12, alpha=.7)
plt.title("Air Passengers Traffic (1949 - 1969)", fontsize=22)
plt.grid(axis='both', alpha=.3)

plt.gca().spines['top'].set_alpha(0.0)
plt.gca().spines['bottom'].set_alpha(0.3)
plt.gca().spines['right'].set_alpha(0.0)
plt.gca().spines['left'].set_alpha(0.3)
plt.show()