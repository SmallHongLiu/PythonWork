'''
Joy Plot允许不同组的密度曲线重叠，这是一种可视化大量分组数据的彼此关系分布的好方法。 它看起来很悦目，并清楚地传达了正确的信息。 它可以使用基于 matplotlib 的 joypy 包轻松构建。
'''

import joypy

# Import Data

mpg = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")



# Draw Plot

plt.figure(figsize=(16,10), dpi= 80)

fig, axes = joypy.joyplot(mpg, column=['hwy', 'cty'], by="class", ylim='own', figsize=(14,10))



# Decoration

plt.title('Joy Plot of City and Highway Mileage by Class', fontsize=22)

plt.show()