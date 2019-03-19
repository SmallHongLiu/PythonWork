import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc

'''
树形图基于给定的距离度量将相似的点组合在一起，并基于点的相似性将它们组织在树状链接中
'''

df = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/USArrests.csv')

plt.figure(figsize=(16, 10), dpi=80)
plt.title("USArrests Dendograms", fontsize=22)
dend = shc.dendrogram(shc.linkage(df[['Murder', 'Assault', 'UrbanPop', 'Rape']], method='ward'), labels=df.State.values, color_threshold=100)
plt.xticks(fontsize=12)
plt.show()
