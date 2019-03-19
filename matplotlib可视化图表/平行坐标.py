import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import parallel_coordinates

'''
平行坐标有助于可视化特征是否有助于有效地隔离组
如果实现隔离，则该特征可能在预测该组时非常有用
'''

df_final = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/diamonds_filter.csv")
plt.figure(figsize=(12, 9), dpi=80)
parallel_coordinates(df_final, 'cut', colormap='Dark2')

plt.gca().spines['top'].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

plt.title('Parallel Coordinated of Diamonds', fontsize=22)
plt.grid(alpha=0.3)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()