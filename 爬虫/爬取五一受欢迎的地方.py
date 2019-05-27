import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

class QuNaEr():
    def __init__(self, keyword, page=1):
        self.keyword = keyword
        self.page = page

    def qne_spider(self):
        url = 'https://piao.qunar.com/ticket/list.htm?keyword=%s&region=&from=mpl_search_suggest&page=%s' % (self.keyword, self.page)
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text
        bs_obj = BeautifulSoup(text, 'html.parser')

        arr = bs_obj.find('div', {'class': 'result_list'}).contents
        for i in arr:
            info = i.attrs
            # 景区名称
            name = info.get('data-sight-name')
            # 地址
            address = info.get('data-address')
            # 近期售票数
            count = info.get('data-sale-count')
            # 经纬度
            point = info.get('data-point')

            # 起始价格
            price = i.find('span', {'class': 'sight_item_price'})
            price = price.find_all('em')
            price = price[0].text

            conn = MongoClient('localhost', post=27017)
            db = conn.QuNaEr  # 库
            table = db.qunaer_51  # 表

            table.insert_one({
                'name'      :   name,
                'address'   :   address,
                'count'     :   int(count),
                'point'     :   point,
                'price'     :   float(price),
                'city'      :   self.keyword
            })


if __name__ == '__main__':
    citys = ['北京', '上海', '成都', '三亚', '广州', '重庆', '深圳', '西安', '杭州', '厦门', '武汉', '大连', '苏州']
    for i in citys:
        for page in range(1, 5):
          qne = QuNaEr(i, page=page)
          qne.qne_spider()


'''
最受欢迎的15个景区的柱状图
'''
from pymongo import MongoClient
# 设置字体，不然会无法显示中文
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']

conn = MongoClient('localhost', port=27017)
db = conn.QuNaEr  # 库
table = db.qunaer_51  # 表

result = table.find().sort([('count', -1)]).limit(15)
# x, y轴数据
x_arr = []  # 景区名称
y_arr = []  # 销售
for i in result:
    x_arr.append(i['name'])
    y_arr.append(i['count'])

'''去哪儿月销售排行榜'''
plt.bar(x_arr, y_arr, color='rgb')  # 指定color，不然所有的主体都会是一个颜色
plt.gcf().autofmt_xdate()  # 旋转x轴，避免重叠
plt.xlabel(u'景点名称')  # x轴描述信息
plt.ylabel(u'月销售')  # y轴描述信息
plt.title(u'拉钩景点月销售统计表')  # 指定图表描述信息
plt.ylim(0, 4000)  # 指定Y轴的高度
plt.savefig('去哪儿月销售排行榜')  # 保存为图片
plt.show()


'''
景区热力图
'''
arr = [[0, 50], [50, 100], [100, 200], [200, 300], [300, 500], [500, 1000]]
name_arr = []
total_arr = []
for i in arr:
    result = table.count({'price', {'$gte': i[0], '$lt': i[1]}})
    name = '%s元 ~ %s元' % (i[0], i[1])
    name_arr.append(name)
    total_arr.append(result)

color = 'red', 'orange', 'green', 'blue', 'gray', 'goldenrod'  # 各类别颜色
explode = (0.2, 0, 0, 0, 0, 0)  # 各类别的偏移半径

# 绘制饼状图
pie = plt.pie(total_arr, colors=color, explode=explode, labels=name_arr, shadow=True, autopct='%1.1f%%')

plt.axis('equal')
plt.title(u'热点旅游景区门票价格比例', fontsize=12)

plt.legend(loc=0, bbox_to_anchor=(0.82, 1))  # 图例
# 设置legend的字体大小
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=6)
# 显示图
plt.show()













