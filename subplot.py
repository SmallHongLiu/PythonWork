import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# fig = plt.figure()

'''
method 1
# 创建小图, 参数为位置描述, 参数1和2表示行列数，参数3表示位置
plt.subplot(2, 2, 1)
plt.plot([0, 1], [0, 1])

plt.subplot(2, 2, 2)
plt.plot([0, 1], [0, 2])

plt.subplot(2, 2, 3)
plt.plot([0, 1], [0, 3])

plt.subplot(2, 2, 4)
plt.plot([0, 1], [0, 4])

plt.subplot(2, 1, 1)
plt.plot([0, 1], [0, 1])

plt.subplot(2, 3, 4)
plt.plot([0, 1], [0, 2])

plt.subplot(2, 3, 5)
plt.plot([0, 1], [0, 3])

plt.subplot(2, 3, 6)
plt.plot([0, 1], [0, 4])
'''

'''
method 2: subplot_grid
'''
'''
# 单元小格, colspan和rowspan:跨度
ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3, rowspan=1)
ax1.plot([1, 2], [1, 2])
ax1.set_xlabel('ax1_title')

ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=1)
ax2.plot([1, 2], [1, 2])
ax2.set_xlabel('ax2_title')

ax3 = plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=2)
ax3.plot([1, 2], [1, 2])
ax3.set_xlabel('ax3_title')

ax4 = plt.subplot2grid((3, 3), (2, 0), colspan=1, rowspan=1)
ax4.plot([1, 2], [1, 2])
ax4.set_xlabel('ax4_title')

ax5 = plt.subplot2grid((3, 3), (2, 1), colspan=1, rowspan=1)
ax5.plot([1, 2], [1, 2])
ax5.set_xlabel('ax5_title')
'''

'''
method 3: gridspec
'''
'''
gs = gridspec.GridSpec(3, 3)
# ':'后面没有数字时表示全部占用
ax1 = plt.subplot(gs[0, :])
ax2 = plt.subplot(gs[1, :2])
ax3 = plt.subplot(gs[1:, 2])
ax4 = plt.subplot(gs[-1, 0])
ax5 = plt.subplot(gs[-1, -2])
'''

'''
method 4
'''
'''
# sharex:恭喜X轴
f, ((ax11, ax12), (ax21, ax22)) = plt.subplots(2, 2, sharex=True, sharey=True)
ax11.scatter([1, 1], [1, 2])
'''

'''图中图'''
'''
x = [1, 2, 3, 4, 5, 6, 7]
y = [1, 3, 4, 2, 5, 8, 6]

# 左下边距
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax1 = fig.add_axes([left, bottom, width, height])
ax1.plot(x, y, 'r')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_title('title')

left, bottom, width, height = 0.2, 0.6, 0.25, 0.25
ax2 = fig.add_axes([left, bottom, width, height])
ax2.plot(y, x, 'b')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('title inside 1')

plt.axes([.6, .2, 0.25, 0.25])
# y[::-1]表示将y的值逆序一下
plt.plot(y[::-1], x, 'g')
plt.xlabel('x')
plt.ylabel('y')
plt.title('title inside 2')
'''

'''主次坐标轴'''
x = np.arange(0, 10, 0.1)
y1 = 0.05 * x ** 2
y2 = -1 * y1

fig, ax1 = plt.subplots()
# 颠倒，镜面, 坐标轴反向
ax2 = ax1.twinx()
ax1.plot(x, y1, 'g-')
ax2.plot(x, y2, 'b--')

ax1.set_xlabel('X data')
ax1.set_ylabel('Y1', color='g')
ax2.set_ylabel('Y2', color='b')


# plt.tight_layout()
plt.show()