import pandas as pd
import numpy as np

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
