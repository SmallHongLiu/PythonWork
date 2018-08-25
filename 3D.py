import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# figure：图片窗口
fig = plt.figure()
# 加一个3D在figurez
ax = Axes3D(fig)
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
# 将x, y值mesh到底面
X, Y = np.meshgrid(X, Y)
# 计算X和Y的值
R = np.sqrt(X ** 2 + Y ** 2)
# 生成高度值
Z = np.sin(R)

# rstride和cstrhid: 跨度（行跨和列跨）， cmap设置等高线颜色值
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
# zdir:压下的方向，即投影的方向, offest: 表示投影到对应坐标轴的哪个值上面
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap='rainbow')
ax.set_zlim(-2, 2)

plt.show()