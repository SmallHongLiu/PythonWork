import matplotlib.pyplot as plt
import numpy as np

# x = np.linspace(-3, 3, 50)
# # y1 = 2 * x + 1
# y1 = 0.1 * x
'''
y2 = x ** 2
# plt.figure()
# plt.plot(x, y1)

plt.figure()
# plt.plot(x, y2)
# plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')

# 设置坐标轴的范围
plt.xlim((-1, 2))
plt.ylim((-2, 3))

# 设置坐标轴的标签
plt.xlabel("I am X")
plt.ylabel("I am Y")

# 设置坐标轴的刻度值
new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3],
            [r'$really\ bad$', 'bad', 'normal', 'good', 'really good'])
'''

# plt.figure(num=1, figsize=(8, 5))
# plt.figure()
# plt.plot(x, y1, lw=10)
# plt.ylim(-2, 2)
#
# ax = plt.gca()
# 'figure的四个边框可以分别作为X和Y轴'
# # 设置坐标轴颜色
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# # 设置表示x和y的坐标轴
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
# # 设置坐标轴的起始点
# ax.spines['bottom'].set_position(('data', 0))
# ax.spines['left'].set_position(('data', 0))

'''
# label：线的名字，用于区分，注意：如果想将线（l1,l2等）传入handlers中的话，必须在其定义后面加上一个逗号
l1, = plt.plot(x, y2, label='up')
l2, = plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--', label='dowm')
# legend: 打印图列，参数：handles：放入legend的线, labels：线在图例中的名字, loc: 位置，'best'自动找一个好的位置（即没有很多数据的区域）
plt.legend(handles=[l1, l2], labels=['aaa', 'bbb'], loc='best')
'''

'''
x0 = 1
y0 = 2 * x0 + 1
# scatter, 参数s(size: 大小），b表示blue
plt.scatter(x0, y0, s=50, color='b')
# plot由两个点画一条直线，k表示黑色，--表示虚线形式的style，linewidth: 线条宽度
plt.plot([x0, x0], [y0, 0], 'k--', lw=2.5)

# method 1
# annotate: 标注, r表示正则表达式,xy: 坐标，从什么位置开始打印这个annotate, xycooords表示前面xy中x0和y0的值，data表示一个基准，xytext是文字描述，其中的+30等是表示文字是基于xy偏移之后显示, textcoords:,
# arrowprops表示指向线
plt.annotate(r'$2x+1=%s$' % y0, xy=(x0, y0), xycoords='data', xytext=(+30, -30), textcoords='offset points',
             fontsize=16, arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

# method 2
# 位置x和y， 文字，字体的style
plt.text(-3.7, 3, r'$This\ is\ the\ some\ text.\ \mu\ \sigma_i\ \alpha_t$',
         fontdict={'size': 16, 'color': 'r'})
'''


# for label in ax.get_xticklabels() + ax.get_yticklabels():
#     label.set_fontsize(12)
#     # facecolor: 前置背景，edgecolor: 边框颜色，alpha：透明度
#     label.set_bbox(dict(facecolor='white', edgecolor='None', alpha=0.7))
#

'''
n = 1024
X = np.random.normal(0, 1, n)
Y = np.random.normal(0, 1, n)

# 点的颜色的随机公式
T = np.arctan2(Y, X)

# scatter：散点图
plt.scatter(X, Y, s=75, c=T, alpha=0.5)

plt.xlim((-1.5, 1.5))
plt.ylim((-1.5, 1.5))

# 当没有参数时，则可以表示隐藏ticks
plt.xticks(())
plt.yticks(())
'''

n = 12
X = np.arange(n)

# uniform：产生一个0.5到1之间产生一个数值，对于每一个n都产生一个
Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)

plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')

# 设置文字标签, 其中zip表示将X和Y1中的值分别传到x和y中
for x, y in zip(X, Y1):
    # 文字标签的位置, ha：horizontal alignment，对其的方式
    plt.text(x, y + 0.05, '%.2f' % y, ha='center', va='bottom')

for x, y in zip(X, Y2):
    plt.text(x, -y - 0.05, '-%.2f' % y, ha='center', va='top')


plt.xlim(-.5, n)
plt.ylim(-1.25, 1.25)

plt.xticks(())
plt.yticks(())

plt.show()