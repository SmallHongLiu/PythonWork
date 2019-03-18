import pandas as pd
import matplotlib.pyplot as plt
import random

df_raw = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")
df = df_raw.groupby('manufacturer').size().reset_index(name='counts')

n = df['manufacturer'].unique().__len__() + 1
all_colors = list(plt.cm.colors.cnames.keys())
random.seed(100)
c = random.choices(all_colors, k=n)

print(all_colors)
print(c)

plt.figure(figsize=(16, 10), dpi=80)
plt.bar(df['manufacturer'], df['counts'], color=c, width=.5)

for i, val in enumerate(df['counts'].values):
    plt.text(i, val, float(val), horizontalalignment='center', verticalalignment='bottom', fontdict={'fontweight': 500, 'size': 12})

plt.gca().set_xticklabels(df['manufacturer'], rotation=60, horizontalalignment='right')
plt.title("Number of Vehicles by Manufacturers", fontsize=22)
plt.ylabel('# Vehicles')
plt.ylim(0, 45)
plt.show()