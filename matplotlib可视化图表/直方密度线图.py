import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

'''
带有直方图的密度曲线汇集了两个图所传达的集体信息，因此您可以将它们放在一个图中而不是两个图中。
'''

df = pd.read_csv('https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv')

plt.figure(figsize=(13, 10), dpi=80)

sns.distplot(df.loc[df['class'] == 'compact', 'cty'], color='dodgerblue', label='Compact', hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
sns.distplot(df.loc[df['class'] == 'suv', "cty"], color="orange", label="SUV", hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
sns.distplot(df.loc[df['class'] == 'minivan', "cty"], color="g", label="minivan", hist_kws={'alpha':.7}, kde_kws={'linewidth':3})

plt.ylim(0, 0.35)

# Decoration
plt.title('Density Plot of City Mileage by Vehicle Type', fontsize=22)
plt.legend()
plt.show()