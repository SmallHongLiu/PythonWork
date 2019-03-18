import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
相关图用于直观地查看给定数据框（或二维数组）中所有可能的数值变量对之间的相关度量。
'''

df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mtcars.csv")

plt.figure(figsize=(12, 10), dpi=80)
sns.heatmap(df.corr(), xticklabels=df.corr().columns, yticklabels=df.corr().columns,
            cmap='RdYlGn', center=0, annot=True)

plt.title('Correlogram of mtcars', fontsize=22)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()