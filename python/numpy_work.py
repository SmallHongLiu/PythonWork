import numpy as np

# 矩阵转换为数组
array = np.array([[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]])

'''
print(array)
# 打印数组的维数
print('number of dim: ', array.ndim)
# 打印数组的行列数
print('shape: ', array.shape)
# 打印数组的大小
print("size: ", array.size)
'''

# 参数2：表示数组的type（类型，如整数，小数等），注：通常位数越大，越精确，但占用空间也越多，通常情况使用64位
# a = np.array([2, 3, 4], dtype=np.int)
# a = np.array([2, 3, 4], dtype=np.float32)
# print(a, a.dtype)

'''
# 定位全部为0的数组, 其中参数分别表示行列数，注意：行列数必须用括号括起来
a = np.zeros((3, 4))
print(a)
a = np.ones((3, 4))
print(a)
a = np.empty((3, 4))
print(a)

# 有序数列，类似于range行数，参数1：起始值，参数2：终止值，参数3：步长，即间距
a = np.arange(10, 20, 2)
print(a)

# arange行数默认是从0开始生成数列，reshape重新定义shape，如这里重新定义为3行4列
a = np.arange(12).reshape((3, 4))
print(a)
'''

'''
# 生成线段，参数1：起始值， 参数2：终止值，参数3：表示需要生成多少线段，会根据此值来自动匹配步长
a = np.linspace(1, 10, 6).reshape((2, 3))
print(a)
'''

'''
a = np.array([10, 20, 30, 40])
b = np.arange(4)
print(a, b)
print(a - b)
print(a + b)

# 双*在python中是表示平方
print(b ** 2)
# 求sin或cos可以直接使用函数
print(10 * np.sin(a))
# 判断数组b中哪些数是小于3的
print(b < 3)
# 判断等于3
print(b == 3)
'''

'''
a = np.array([[1, 1], [0, 1]])
b = np.arange(4).reshape((2, 2))
print(a)
print(b)
# 逐个相乘
c = a * b
print(c)
# 矩阵中的乘法
c_dot = np.dot(a, b)
# 该方法和上面的效果是相同的
c_dot_2 = a.dot(b)
print(c_dot)
print(c_dot_2)
'''

'''
a = np.random.random((2, 4))
print(a)
# 求和，其中参数axis表示维度，如果没有，则默认为全部，如果为1，则表示在列数中计算，如果为0，则表示在行数中计算
print(np.sum(a, axis=1))
# 求最小值
print(np.min(a, axis=0))
# 求最大值
print(np.max(a, axis=1))
'''
'''
# arange的参数表示起始值和终止值,注：包含起始值但不包含起始值
A = np.arange(2, 14).reshape((3, 4))
print(A)
# 查找最小值的索引，即下标
print(np.argmin(A))
# 查找最大值的索引
print(np.argmax(A))
# 求平局值，下面集中方法效果相同
print(np.mean(A))
print(A.mean())
print(np.average(A))

# 求中位数
print(np.median(A))

# 累加, 当前位置前面的所有和加上该位置的值
print(np.cumsum(A))

# 求差, 当前数和上一个数的差
print(np.diff(A))
# 第一个array表示行数，第二个array表示列数
print(np.nonzero(A))
'''

'''
A = np.arange(14, 2, -1).reshape(3, 4)
print(A)
# 逐行排序
print(np.sort(A))
# 矩阵反向
print(np.transpose(A))
print(A.T)
print((A.T).dot(A))

# 截取数据, 参数2：最小值，参数3：最大值，表示该数组中，从最小值开始，所有小于最小值的数都变为最小值，从最大值开始，所有大于最大值的数都变为最大值，然后中间的数不改变其值
print(np.clip(A, 5, 9))
'''

'''注意，基本所有的numpy指令基本都可以指定其行列（aixs, 0: 对列计算，1：对行计算)'''

'''
A = np.arange(3, 15)
print(A)
# 根据索引查找值
print(A[3])
'''
'''
A = np.arange(3, 15).reshape((3, 4))
print(A)
# 索引出某一行的数据
print(A[2])
# 索引出某一行某一列对应的数值, 下面两种表示方式相同
print(A[1][1])
print(A[1, 1])
# 某一行，从哪个位置到哪个位置的数据, 如：第一行中，从1到3的数据
print(A[1, 1:3])

# 遍历行
for row in A:
    print(row)

# 遍历列, 通过反向矩阵，然后遍历其行来实现
for column in A.T:
    print(column)

# 输出一个迭代器的值
print(A.flatten())
# A.flat表示一个迭代器, 遍历每个项
for item in A.flat:
    print(item)
'''

'''
A = np.array([1, 1, 1])
B = np.array([2, 2, 2])
# 合并数列，上下合并，垂直合并
C = np.vstack((A, B))
print(C)
# 左右合并, 水平合并
D = np.hstack((A, B))
print(D)
print(A.shape, D.shape)
print(A)
# newaxis表示新增一个维度, 参数1为行维度，参数2为列维度，可以不填值，用：隔开就行
print(A[np.newaxis, np.newaxis])
print(A[:, np.newaxis])
print(A[np.newaxis, :])
'''

'''
A = np.array([1, 1, 1])[:, np.newaxis]
B = np.array([2, 2, 2])[:, np.newaxis]
print(np.hstack((A, B)))
print(np.hstack((A, A, B)))
# concatenate方法可以定义合并的维度的方向, 0表示纵向合并，1表示横向合并
C = np.concatenate((A, B, B, A), axis=1)
print(C)
'''

'''
A = np.arange(12).reshape((3, 4))
print(A)
# 横向分割, 参数1表示要分割的数列，参数2表示要分割成几块，axis表示分割的方向
# print(np.split(A, 2, axis=1))

# 注意，只能进行相等的分割，即下面的这行代码会报错
# print(np.split(A, 3, axis=1))

# array_split可以进行不相等的分割
print(np.array_split(A, 3, axis=1))

# 纵向分割
print(np.vsplit(A, 3))
# 横向分割
print(np.hsplit(A, 2))
'''

'''
a = np.arange(4)
print(a)
# 注意，python中，array的赋值是相当于浅拷贝，也可以成为关联，即b, c, d就相当于是a本身, 如果改变a的值，其它的值也会改变，如果改变b, c, d中的值，a中的值也会改变，
b = a
c = a
d = b
a[0] = 3
print(a)
print(b)
print(c)
print(c)

# deep copy，深拷贝，只拷贝值，不关联，这种情况如果改变其中一个的值，另外一个的值是不会改变的
b = a.copy()
'''


