from pyecharts import Pie
from pyecharts import Bar
from pyecharts import TreeMap
from pyecharts import Scatter


# 性别饼状图分析
def create_gender(df):
    df = df.copy()
    df.loc[df.gender == 0, 'gender'] = '未知'
    df.loc[df.gender == 1, 'gender'] = '男性'
    df.loc[df.gender == 2, 'gender'] = '女性'
    gender_message = df.groupby(['gender'])
    gender_com = gender_message['gender'].age(['count'])
    gender_com.reset_index(inplace=True)

    # 生成饼状图
    attr = gender_com['gender']
    v1 = gender_com['count']
    pie = Pie('抖音大V性别分布情况', title_pos='center', title_top=0)
    pie.add('', attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True,
            legend_orient='vertical', legend_pos='left', legend_top='%10')
    pie.render('抖音大V性别分布情况.html')


# 生成点赞数top10的柱状图
def create_links(df):
    '''点赞数'''
    df = df.sort_values('links', acending=False)
    attr = df['name'][0:10]
    v1 = ['{}'.format(float('%.1f' % (float(i) / 100000000))) for i in df['links'][0:10]]

    # 柱状图
    bar = Bar('抖音大V点赞数Top10(亿)', title_pos='center', title_top='18', width=800, height=400)
    bar.add('', attr, v1, is_convert=True, xaxis_min=0, yaxis_label_textsize=12, is_yaxis_boundarygap=True,
            yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right', is_yaxis_inverse=True,
            is_splitline_show=False)
    bar.render('抖音大V点赞数TOP10.html')


# 生成粉丝数top10的柱状图
def create_fans(df):
    """
    粉丝数
    """
    df = df.sort_values('fans', ascending=False)
    attr = df['name'][0:10]
    v1 = ["{}".format(float('%.1f' % (float(i) / 10000))) for i in df['fans'][0:10]]

    # 生成柱状图
    bar = Bar("抖音大V粉丝数TOP10(万)", title_pos='center', title_top='18', width=800, height=400)
    bar.add("", attr, v1, is_convert=True, xaxis_min=0, yaxis_label_textsize=12, is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right', is_yaxis_inverse=True, is_splitline_show=False)
    bar.render("抖音大V粉丝数TOP10.html")


# 点赞数汇总分布
def create_type_links(df):
    '''类型点赞数'''
    dom = []
    likes_type_message = df.groupby(['type'])
    likes_type_com = likes_type_message['likes'].agg(['sum'])
    likes_type_com.reset_index(inplace=True)
    for name, num in zip(likes_type_com['type'], likes_type_com['sum']):
        data = {}
        data['name'] = name
        data['value'] = num
        dom.append(data)
    # 生成矩形树图
    treemap = TreeMap("各类型抖音大V点赞数汇总图", title_pos='center', title_top='5', width=800, height=400)
    treemap.add('各类型抖音大V点赞数汇总图', dom, is_label_show=True, label_pos='inside', is_legend_show=False)
    treemap.render('各类型抖音大V点赞数汇总图.html')


# 粉丝数汇总分布
def create_type_fans(df):
    '''类型粉丝数'''
    dom = []
    fans_type_message = df.groupby(['type'])
    fans_type_com = fans_type_message['fans'].agg(['sum'])
    fans_type_com.reset_index(inplace=True)
    for name, num in zip(fans_type_com['type'], fans_type_com['sum']):
        data = {}
        data['name'] = name
        data['value'] = num
        dom.append(data)

    # 生成矩形树图
    treemap = TreeMap("各类型抖音大V粉丝数汇总图", title_pos='center', title_top='5', width=800, height=400)
    treemap.add('各类型抖音大V粉丝数汇总图', dom, is_label_show=True, label_pos='inside', is_legend_show=False)
    treemap.render('各类型抖音大V粉丝数汇总图.html')


# 视频粉丝点赞数三维度
def create_scatter(df):
    '''三维度散点图'''
    data = [list(i) for i in zip(df['videos'], df['fans'], df['likes'], df['name'])]

    # 生成散点图
    x_lst = [v[0] for v in data]
    y_lst = [v[1] for v in data]
    extra_data = [v[2] for v in data]
    sc = Scatter('抖音大V视频粉丝数点赞数三维度', title_pos='center', title_top='5', width=800, height=400)
    sc.add('', x_lst, y_lst, extra_data=extra_data, is_visualmap=True, visual_dimensiton=2, visual_orient="horizontal", visual_type="size", visual_range=[0, 500000000], visual_text_color="#000", visual_range_size=[5, 30])
    sc.render('抖音大V视频数粉丝数点赞数三维度.html')


# 平均点赞数柱状图
def create_awg_likes(df):
    '''平均点赞数'''
    df = df[df['videos'] > 0]
    df.eval('result=likes/(videos*10000)', inplace=True)
    df['result'] = df['result'].round(decimals=1)
    df = df.sort_values('result', ascending=False)
    attr = df['name'][0:10]
    v1 = df['result'][0:10]

    # 生成柱状图
    bar = Bar('抖音大V平均视频点赞数top10(万)', title_pos='center', title_top='18', width=800, height=400)
    bar.add('', attr, v1, is_convert=True, xaxis_min=0, yaxis_label_textsize=12, is_yaxis_boundarygap=True,
            yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right', is_yaxis_inverse=True, is_splitline_show=False)
    bar.render('抖音大V平均视频点赞数top10.html')


# 平均视频粉丝数top10
def create_avg_fans(df):
    '''平均粉丝数'''
    df = df[df['videos'] > 0]
    df.eval('result=fans/(videos*10000)', inplace=True)
    df['result'] = df['result'].round(decimals=1)
    df = df.sort_values('result', ascending=False)
    attr = df['name'][0:10]
    v1 = df['result'][0:10]

    # 生成柱状图
    bar = Bar('抖音大V平均视频粉丝数TOP10(万)')
    bar.add('', attr, v1, is_convert=True, xaxis_min=0, yaxis_label_text_size=12, is_yaxis_boundarygap=True, yaxis_interval=0, is_label_show=True, is_legend_show=False, label_pos='right', is_yaxis_inverse=True, is_splitline_show=False)
    bar.render('抖音大V平均视频粉丝数Top10.html')














