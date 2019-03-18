import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv")
df_counts = df.groupby(['hwy', 'cty']).size().reset_index(name='counts')

fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
# 避免点重叠问题的另一个选择是增加点的大小，这取决于该点中有多少点，点的大小越大，其周围的点的集中度越高
sns.stripplot(df_counts.cty, df_counts.hwy, size=df_counts.counts*2, ax=ax)

plt.title('Counts Plot - Size of circle is bigger as more points overlap', fontsize=22)

plt.show()