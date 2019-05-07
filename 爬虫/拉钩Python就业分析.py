import json
import requests
import xlwt
import time

# 获取存储职位信息的json对象，遍历获得公司名，福利待遇，工作地点，学历要求，工作类型，发布时间，职位名称，薪资，工作年限
def get_json(url, datas):
    my_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        "Referer": "https://www.lagou.com/jobs/list_Python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",
        "Content-Type": "application/x-www-form-urlencoded;charset = UTF-8"
    }

    time.sleep(5)

    ses = requests.sessions()  # 获取session
    ses.headers.update(my_headers)  # 更新
    ses.get("https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=")

    content = ses.post(url=url, data=datas)
    result = content.json()
    info = result['content']['positionResult']['result']
    info_list = []
    for job in info:
        information = []
        information.append(job['positionId'])  # 岗位id
        information.append(job['city'])  # 岗位对应城市
        information.append(job['companyFullName'])  # 公司全名
        information.append(job['companyLabelList'])  # 福利待遇
        information.append(job['district'])  # 工作地点
        information.append(job['education'])  # 学历要求
        information.append(job['firstType'])  # 工作类型
        information.append(job['formatCreateTime'])  # 发布时间
        information.append(job['positionName'])  # 职位名称
        information.append(job['salary'])  # 薪资
        information.append(job['workYear'])  # 工作年限
        info_list.append(information)
        # 将列表对象进行json格式的编码转换,其中indent参数设置缩进值为2
        # print(json.dumps(info_list, ensure_ascii=False, indent=2))

    # print(info_list)
    return info_list

def main():
    page = int(input('请输入你要抓取的页码总数: '))
    kd = input('请输入你要抓取的职位关键字: ')
    city = input('请输入你要抓取的城市: ')

    info_result = []
    title = ['岗位id', '城市', '公司全名', '福利待遇', '工作地点', '学历要求', '工作类型', '发布时间', '职位名称', '薪资', '工作年限']
    info_result.append(title)
    for x in range(1, page+1):
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        datas = {
            'first': 'false',
            'pn': x,
            'kd': 'python',
        }
        try:
            info = get_json(url, datas)
            info_result = info_result + info
            print('第%s页正常采集' % x)
        except Exception as msg:
            print('第%s页出现问题' % x)

        # 创建workbook，即excel
        workbook = xlwt.Workbook(encoding='utf-8')
        # 创建表，第二参数用于确认同一个cell单元是否可以重设值
        worksheet = workbook.add_sheet('lagouzp', cell_overwrite_ok=True)

        for i, row in enumerate(info_result):
            for j, col in enumerate(row):
                worksheet.write(i, j, col)
        workbook.save('lagouzp.xls')


if __name__ == '__main__':
    main()


from pyecharts import Bar

city_nms_top10 = ['北京', '上海', '深圳', '成都', '杭州', '广州', '武汉', '南京', '苏州', '郑州', '天津', '西安', '东莞', '珠海', '合肥', '厦门', '宁波',
                  '南宁', '重庆', '佛山', '大连', '哈尔滨', '长沙', '福州', '中山']
city_nums_top10 = [149, 95, 77, 22, 17, 17, 16, 13, 7, 5, 4, 4, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

bar = Bar('Python岗位', '各城市数量')
bar.add('数量', city_nms, city_nums, is_more_utils=True)
bar.render('Python岗位各城市数量.html')


'''
地图分布展示
'''
from pyecharts import Geo

city_datas = [('北京', 149), ('上海', 95), ('深圳', 77), ('成都', 22), ('杭州', 17), ('广州', 17), ('武汉', 16), ('南京', 13), ('苏州', 7),
     ('郑州', 5), ('天津', 4), ('西安', 4), ('东莞', 3), ('珠海', 2), ('合肥', 2), ('厦门', 2), ('宁波', 1), ('南宁', 1), ('重庆', 1),
     ('佛山', 1), ('大连', 1), ('哈尔滨', 1), ('长沙', 1), ('福州', 1), ('中山', 1)]
geo = Geo('Python岗位城市分布地图', '数据来源拉钩', title_color='#fff',
          title_pos='center', width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(city_datas)
geo.add('', attr, value, visual_range=[0, 200], visual_text_color='#fff',
        symbol_size=15, is_visualmap=True)
geo.render('Python岗位城市分布地图_scatter.html')

geo = Geo('Python岗位城市分布地图', '数据来源拉钩', title_color='#fff',
          title_pos='center', width=1200, height=600, background_color='#404a59')
attr, value = geo.cast(city_datas)
geo.add('', attr, value, type='heatmap', visual_range=[0, 10], visual_text_color='#fff',
        symbol_size=15, is_visualmap=True)
geo.render('Python岗位城市分布地图_heatmap.html')

from pyecharts import Pie

city_nms_top10 = ['北京', '上海', '深圳', '成都', '广州', '杭州', '武汉', '南京', '苏州', '郑州']
city_nums_top10 = [149, 95, 77, 22, 17, 17, 16, 13, 7, 5]
pie = Pie()
pie.add('', city_nms_top10, city_nums_top10, is_label_show=True)
pie.render('Python岗位各城市分布饼图.html')
