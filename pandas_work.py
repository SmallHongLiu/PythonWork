import pandas as pd
import numpy as np

'''
s = pd.Series([1, 3, 6, np.nan, 44, 1])
print(s)

dates = pd.date_range('20180101', periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=['a', 'b', 'c', 'd'])
print(df)

df1 = pd.DataFrame(np.arange(12).reshape((3, 4)))
print(df1)

# 字典的形式
df2 = pd.DataFrame({'A': 1.,
                    'B': pd.Timestamp('20130101'),
                    'C': pd.Series(1, index=list(range(4)),dtype='float32'),
                    "D": np.array([3] * 4, dtype='int32'),
                    'E': pd.Categorical(['test', 'train', 'test', 'train']),
                    'F': 'foo'})
print(df2)
print(df2.dtypes)
print(df2.index)
print(df2.columns)
print(df2.values)
# 描述, 只用于数字的描述，其中类似date和字符串类似的是不起作用的
print(df2.describe())
# 按照index 进行排序, 其中ascending 表示排序的顺序，倒序或正序, False表示倒序，True表示正序
print(df2.sort_index(axis=1, ascending=False))
# 对values进行排序，其中参数by表示对哪一个进行排序
print(df2.sort_values(by='E'))
'''

# dates = pd.date_range('20130101', periods=6)
# df = pd.DataFrame(np.arange(24).reshape((6, 4)), index=dates, columns=['A', 'B', "C", 'D'])

'''
# 选择某一列的数据, 下面两行代码效果类似
print(df['A'])
print(df.A)

# 切片选择，即从第*行到第*行进行选择
print(df[0:3])
print(df['2013-01-02': '2013-01-03'])
'''

# print(df)

'''
# select by label: loc
print(df.loc['20130102'])
# 保留所有行，选择某些列
print(df.loc[:, ['A', 'B']])
'''

'''
# select by position: iloc
# 选择某一行的所有数据
print(df.iloc[3])
# 选择某一行某一列的指定项
print(df.iloc[3, 1])
# 切片筛选
print(df.iloc[3:5, 1:3])
# 逐个筛选
print(df.iloc[[1, 3, 5], 1:3])
'''

'''
# mixed selection:ix
print(df.ix[:3, ['A', 'C']])

# Boolean indexing
# 筛选出某一列中大于某个值的所有数据
print(df[df.A > 8])
print(df[df.A < 8])
'''

'''
# iloc相当于根据位置进行选择
df.iloc[2, 2] = 11
# loc通过标签获取值
df.loc['20130101', 'B'] = 22
# 将某一列中的数据中大于某个数的值修改为某个值
# df[df.A > 4] = 0
# 将B标签中对应的A标签的值大于4的值修改为99
df.B[df.A > 4] = 99
# 新增一列值全部为NaN
df['F'] = np.nan
# 新增一列，其为序列
df['E'] = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range('20130101', periods=6))
print(df)
'''

'''
df.iloc[0, 1] = np.nan
df.iloc[1, 2] = np.nan
print(df)

# dropna按照行中有nan即丢掉, how表示什么情况, 其值any表示任一个满足，all表示全部满足
print(df.dropna(axis=0, how='any'))
# 丢掉列
print(df.dropna(axis=1, how='any'))

# 填充数据, value表示想要填充的值
print(df.fillna(value=0))
# 判断是否有缺失（丢失) 数据
print(df.isnull)
# 判断其中是否有数据丢失，如果有，则会为True，np.any(df.isnull())表示任何一个为丢失
# 该方法可以用于当数据表格很大时，查找是否有数据丢失
print(np.any(df.isnull()) == True)
'''

'''
# csv 还可以读取txt的，注意：panads读取时会自动添加索引
data = pd.read_csv('/users/small_hong/ExcelProjects/python/student.csv')
print(data)
# 导出数据
data.to_pickle('/users/small_hong/ExcelProjects/python/student.pickle')
'''

'''
# concatenating
df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3, 4)) * 2, columns=['a', 'b', 'c', 'd'])
print(df1)
print(df2)
print(df3)
# 0：竖向合并, 1: 横向合并, ignore_index：忽略index重新排序
res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)
print(res)
'''

'''
# join, ['inner', 'outer']
df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['b', 'c', 'd', 'e'], index=[2, 3, 4])
print(df1)
print(df2)
# 这样合并，如果行列不相同时，会自动以Nan填充
# res = pd.concat([df1, df2])
# join默认值为outter，即填充合并，而inner表示裁剪合并
# res = pd.concat([df1, df2], join='inner', ignore_index=True)
# print(res)

res = pd.concat([df1, df2], axis=1, join_axes=[df1.index])
print(res)
'''

df1 = pd.DataFrame(np.ones((3, 4)) * 0, columns=['a', 'b', 'c', 'd'])
df2 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['a', 'b', 'c', 'd'])
df3 = pd.DataFrame(np.ones((3, 4)) * 1, columns=['b', 'c', 'd', 'e'], index=[2, 3, 4])

# 将某个数组加到某个数组上，将df2加上df1中
# res = df1.append(df2, ignore_index=True)
# res = df1.append([df2, df3])
s1 = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])
res = df1.append(s1, ignore_index=True)
print(res)
