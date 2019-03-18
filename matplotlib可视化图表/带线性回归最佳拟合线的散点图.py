import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv")

df_select = df.loc[df.cyl.isin([4, 8]), :]

sns.set_style('white')

'''
# lmplot：回归图，对所选数据集进行了一元线性回归，拟合出一条最佳的直线，其可以直观地总揽数据的内在关系
# lmplot参数说明：hue：用于分类；aspect：控制图的长宽比；
gridobj = sns.lmplot(x='displ', y='hwy', hue='cyl', data=df_select,
                     height=7, aspect=1.6, robust=True, palette='tab10',
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))

gridobj.set(xlim=(0.5, 7.5), ylim=(0, 50))

plt.title("Scatterplot with line of best fit grouped by number of cylinders", fontsize=20)

plt.show()
'''

# 针对每列绘制线性回归线
gridobj = sns.lmplot(x='displ', y='hwy', data=df_select,
                     height=7, robust=True, palette='Set1', col='cyl',
                     scatter_kws=dict(s=60, linewidths=.7, edgecolors='black'))
gridobj.set(xlim=(0.5, 7.5), ylim=(0, 50))

plt.show()