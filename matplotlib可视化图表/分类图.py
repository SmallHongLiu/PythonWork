import seaborn as sns
import matplotlib.pyplot as plt

'''
由 seaborn库 提供的分类图可用于可视化彼此相关的2个或更多分类变量的计数分布。
'''

titanic = sns.load_dataset('titanic')

g = sns.catplot('alive', col='deck', col_wrap=4,
                data=titanic[titanic.deck.notnull()],
                kind='count', height=3.5, aspect=.8,
                palette='tab20')

plt.show()

titanic = sns.load_dataset('titanic')

sns.catplot(x='age', y='embark_town',
            hue='sex', col='class',
            data=titanic[titanic.embark_town.notnull()],
            orientation='h', height=5, aspect=1, palette='tab10',
            kind='violin', dodge=True, cut=0, bw=.2)