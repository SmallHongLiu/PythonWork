import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

midwest = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/midwest_filter.csv")

categories = np.unique(midwest['category'])
colors = [plt.cm.tab10(i/float(len(categories) - 1)) for i in range(len(categories))]

plt.figure(figsize=(16, 10), dpi=80, facecolor='w', edgecolor='k')

# enumerate 函数用于将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
for i, categore in enumerate(categories):
    plt.scatter('area', 'poptotal',
                data=midwest.loc[midwest.category == categore, :],
                s = 20, cmap=colors[i], label=str(categore))

plt.gca().set(xlim=(0.0, 0.1), ylim=(0, 90000),
              xlabel='Area', ylabel='Population')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Scatterplot of Midwest Area vs Population", fontsize=22)
plt.legend(fontsize=12)
plt.show()