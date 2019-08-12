import matplotlib.pyplot as plt
import numpy as np

def f(x, y):
    # 根据x, y的值计算高度
    return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)

n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)

# 网格
X, Y = np.meshgrid(x, y)

# 放入颜色在等高线, 其中8表示等高线的高度分成了多少份
plt.contourf(X, Y, f(X, Y), 8, alpha=0.75, cmap=plt.cm.hot)

# 画等高线
C = plt.contour(X, Y, f(X, Y), 8, color='black', linewidth=.5)

# 加上数字描述
plt.clabel(C, inline=True, fontsize=10)

plt.xticks(())
plt.yticks(())
plt.show()

