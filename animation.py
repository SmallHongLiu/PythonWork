import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig, ax = plt.subplots()

x = np.arange(0, 2 * np.pi, 0.01)
# 生成一条直线
line, = ax.plot(x, np.sin(x))

def animate(i):
    line.set_ydata(np.sin(x + i / 10))
    return line,

def init():
    line.set_ydata(np.sin(x))
    return line,

# 产生动画, frames表示长度，帧数, init_func表示初始帧，interval表示频率，即多久更新一次, blit表示是否更新整张图的点, 注意，此处mac必须设置为false,不然没有效果
ani = animation.FuncAnimation(fig= fig, func=animate, frames=100, init_func=init, interval=20, blit=False)
plt.show()