import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
密度图是一种常用工具，用于可视化连续变量的分布。
通过“响应”变量对它们进行分组，您可以检查 X 和 Y 之间的关系。
以下情况用于表示目的，以描述城市里程的分布如何随着汽缸数的变化而变化。
'''

df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")

plt.figure(figsize=(16, 10), dpi=80)

sns.kdeplot(df.loc[df['cyl'] == 4, 'cty'], shade=True, color='g', label='Cyl=4', alpha=.7)
sns.kdeplot(df.loc[df['cyl'] == 5, 'cty'], shade=True, color='deeppink', label='Cyl=5', alpha=.7)
sns.kdeplot(df.loc[df['cyl'] == 6, 'cty'], shade=True, color='dodgerblue', label='Cyl=6', alpha=.7)
sns.kdeplot(df.loc[df['cyl'] == 8, 'cty'], shade=True, color='orange', label='Cyl=8', alpha=.7)

plt.title('Density Plot of City Mileage by n_Cylinders', fontsize=22)
plt.legend()
plt.show()