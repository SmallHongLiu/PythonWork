import pandas as pd
import matplotlib.pyplot as plt
import calmap

'''
与时间序列相比，日历地图是可视化基于时间的数据的备选和不太优选的选项
虽然可以在视觉上吸引人，但数值并不十分明显
然而，它可以很好地描绘极端值和假日效果
'''

df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/yahoo.csv", parse_dates=['date'])
df.set_index('date', inplace=True)

plt.figure(figsize=(16, 10), dpi=80)
calmap.calendarplot(df['2014']['VIX.Close'], fig_kws={'figsize': (16, 10)}, yearlabel_kws={'color': 'black', 'fontsize':14}, subplot_kws={'title':'Yahoo Stock Prices'})
plt.show()