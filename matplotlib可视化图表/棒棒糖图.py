import pandas as pd
import matplotlib.pyplot as plt

'''
棒棒糖图表以一种视觉上令人愉悦的方式提供与有序条形图类似的目的。
'''

df_raw = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")
df = df_raw[['cty', 'manufacturer']].groupby('manufacturer').apply(lambda x: x.mean())
df.reset_index(inplace=True)

fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
ax.vlines(x=df.index, ymin=0, ymax=df.cty, color='firebrick', alpha=0.7, linewidth=2)
ax.scatter(x=df.index, y=df.cty, s=75, color='firebrick', alpha=0.7)

ax.set_title('Lollipop Chart for Highway Mileage', fontdict={'size':22})
ax.set_ylabel('Miles Per Gallon')
ax.set_xticks(df.index)
ax.set_xticklabels(df.manufacturer.str.upper(), rotation=60, fontdict={'horizontalalignment': 'right', 'size': 12})
ax.set_ylim(0, 30)

for row in df.itertuples():
    ax.text(row.Index, row.cty+0.5, s=round(row.cty, 2), horizontalalignment='center', verticalalignment='bottom', fontsize=14)

plt.show()