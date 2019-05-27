# coding=utf-8
'''
Author: Small_Hong
date: 2019-05-21 $ {TIME}
'''

import plotly
import plotly.offline as py
import numpy as np
import plotly.graph_objs as go

# 设置 offline
plotly.offline.init_notebook_mode(connected=False)

"""
N = 100
random_x = np.linespace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

trace0 = go.Scatter(
    x=random_x,
    y=random_y0,
    mode='markers',
    name='markers'
)

trace1 = go.Scatter(
    x=random_x,
    y=random_y1,
    mode='lines+markers',
    name='lines+markers'
)

trace2 = go.Scatter(
    x=random_x,
    y=random_y2,
    mode='lines',
    name='lines'
)

data = [trace0, trace1, trace2]
"""

'''
# 气泡图
data = [
    {
        'x': [1, 3.2, 5.4, 7.6, 9.8, 12.5],
        'y': [1, 3.2, 5.4, 7.6, 9.8, 12.5],
        'mode': 'markers',
        'marker': {
            'color': [120, 125, 130, 135, 140, 145],
            'size': [15, 30, 55, 70, 90, 110],
            'showscale': True
        }
    }
]
py.iplot(data)
'''

import plotly_express as px
import plotly
import plotly.graph_objs as go
plotly.offline.init_notebook_mode(connected=True)

iris = px.data.iris()

iris_plot = px.scatter(iris, x='sepal_width', y='sepal_length',
           color='species', marginal_y='histogram',
          marginal_x='box', trendline='ols')

plotly.offline.plot(iris_plot)




