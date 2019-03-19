import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

'''
自相关图（ACF图）显示时间序列与其自身滞后的相关性
每条垂直线（在自相关图上）表示系列与滞后0之间的滞后之间的相关性
图中的蓝色阴影区域是显着性水平。 那些位于蓝线之上的滞后是显着的滞后
'''

df = pd.read_csv('https://github.com/selva86/datasets/raw/master/AirPassengers.csv')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=80)
plot_acf(df.value.tolist(), ax=ax1, lags=50)
plot_pacf(df.value.tolist(), ax=ax2, lags=20)

ax1.spines['top'].set_alpha(.3);
ax1.spines['bottom'].set_alpha(.3);
ax1.spines['right'].set_alpha(.3);
ax1.spines['left'].set_alpha(.3);

ax2.spines['top'].set_alpha(.3);
ax2.spines['bottom'].set_alpha(.3);
ax2.spines['right'].set_alpha(.3);
ax2.spines['left'].set_alpha(.3);

ax1.tick_params(axis='both', labelsize=12)
ax2.tick_params(axis='both', labelsize=12)
plt.show()