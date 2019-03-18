import pandas as pd
import matplotlib.pyplot as plt

'''
与发散型条形图 （Diverging Bars）相比，条的缺失减少了组之间的对比度和差异
'''

df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mtcars.csv")

x = df.loc[:, ['mpg']]

df['mpg_z'] = (x - x.mean()) / x.std()
df['colors'] = ['red' if x < 0 else 'darkgreen' for x in df['mpg_z']]
df.sort_values('mpg_z', inplace=True)
df.reset_index(inplace=True)

plt.figure(figsize=(8, 10), dpi=80)
plt.scatter(df.mpg_z, df.index, s=450, alpha=.6, color=df.colors)
for x, y, tex in zip(df.mpg_z, df.index, df.mpg_z):
    plt.text(x, y, round(tex, 1), horizontalalignment='center',
             verticalalignment='center', fontdict={'color': 'white'})

plt.gca().spines['top'].set_alpha(.3)
plt.gca().spines['bottom'].set_alpha(.3)
plt.gca().spines['right'].set_alpha(.3)
plt.gca().spines['left'].set_alpha(.3)

plt.yticks(df.index, df.cars)
plt.title('Diverging Dotplot of Car Mileage', fontdict={'size':20})
plt.xlabel('$Mileage$')
plt.grid(linestyle='--', alpha=0.5)
plt.xlim(-2.5, 2.5)
plt.show()

