import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
小提琴图是箱形图在视觉上令人愉悦的替代品。 小提琴的形状或面积取决于它所持有的观察次数。 
但是，小提琴图可能更难以阅读，并且在专业设置中不常用。
'''

df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")

plt.figure(figsize=(13, 10), dpi=80)

sns.violinplot(x='class', y='hwy', data=df, scale='width', inner='quartile')

plt.title('Violin Plot of Highway Mileage by Vehicle Class', fontsize=22)
plt.show()


