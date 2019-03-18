import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://raw.githubusercontent.com/selva86/datasets/master/mpg_ggplot2.csv")

fig, ax = plt.subplots(figsize=(16, 10), dpi=80)
# stripplot：避免多个相同点重叠，将相同数据点稍微抖动
# stripplot的作图原理：按照x属性所对应的类别分别展示y属性的值，适用于分类数据
# 参数说明：x：设置分组统计字段；y：设置分布统计字段；jitter：当数据点重合较多时，可用该参数做一些调整
sns.stripplot(df.cty, df.hwy, jitter=0.25, size=8, ax=ax, linewidth=.5)

plt.title('Use jittered plots to avoid overlapping of points', fontsize=22)

plt.show()