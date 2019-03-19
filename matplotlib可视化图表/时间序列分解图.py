import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse

'''
时间序列分解图显示时间序列分解为趋势，季节和残差分量
'''

df = pd.read_csv('https://github.com/selva86/datasets/raw/master/AirPassengers.csv')
dates = pd.DatetimeIndex([parse(d).strftime('%y-%m-01') for d in df['date']])
df.set_index(dates, inplace=True)

result = seasonal_decompose(df['value'], model='multiplicative')

plt.rcParams.update({'figure.figsize': (10, 10)})
result.plot().suptitle('Time Series Decomposition of Air Passengers')
plt.show()