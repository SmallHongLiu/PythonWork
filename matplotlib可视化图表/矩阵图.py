import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('iris')

plt.figure(figsize=(10, 8), dpi=80)

# sns.pairplot(df, kind='scatter', hue='species', plot_kws=dict(s=80, edgecolor='white'))
sns.pairplot(df, kind='reg', hue='species')

plt.show()
