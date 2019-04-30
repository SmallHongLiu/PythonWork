import requests
import json
import time
import pandas as pd
import random


# 页面基本信息解析，获取构成弹幕网址所需的后缀ID，播放量，集数等信息
def parse_base_info(url, headers):
    df = pd.DataFrame()

    html = requests.get(url, headers=headers)
    bs = json.loads(html.text[html.text.find('{'):-1])

    for i in bs['results']:
        # 后缀ID
        v_id = i['id']
        # 这一集的名字，比如"都挺好_01'
        title = i['fields']['title']
        # 播放量
        view_count = i['fields']['view_all_count']
        # 整型存储的集数，片花则为0
        episode = int(i['fields']['episode'])
        # 去掉片花，只留下正片
        if episode == 0:
            pass
        else:
            cache = pd.DataFrame({'id': [v_id], 'title': [title], '播放量': [view_count], "第几集": [episode]})
            df = pd.concat([df, cache])
    return df


# 传入后缀ID，获取该集的target_id并返回
def get_episode_danmu(v_id, headers):
    base_url = 'https://access.video.qq.com/danmu_manage/regist?vappid=97767206&vsecret=c0bdcbae120669fff425d0ef853674614aa659c605a613a4&raw=1'
    pay = {"wRegistType": 2, "vecIdList": [v_id],
           "wSpeSource": 0, "bIsGetUserCfg": 1,
           "mapExtData": {v_id: {"strCid": "wu1e7mrffzvibjy", "strLid": ""}}}

    html = requests.post(base_url, data=json.dumps(pay), headers=headers)
    bs = json.loads(html.text)
    # 定位元素
    danmu_key = bs['data']['stMap'][v_id]['strDanMuKey']
    # 解析出target_id
    target_id = danmu_key[danmu_key.find('targetid') + 9: danmu_key.find('vid') - 1]
    return [v_id, target_id]


# 解析单个弹幕页面，需要传入target_id，v_id(后缀ID)和集数(方便匹配),返回具体的弹幕信息
def parse_danmu(url, target_id, v_id, headers, period):
    html = requests.get(url, headers=headers)
    bs = json.loads(html.text, strict=False)  # strict参数：避免部分内容因为格式问题出现解析问题

    # 存储数据
    df = pd.DataFrame()
    # 遍历获取目标字段
    for i in bs['comments']:
        content = i['content']
        name = i['opername']
        up_count = i['upcount']
        user_degree = i['uservip_degree']
        time_point = i['timepoint']
        comment_id = i['commentid']
        cache = pd.DataFrame({"用户名": [name], "内容": [content], '会员等级': [user_degree],
                              '评论时间点': [time_point], '评论点赞数': [up_count], '评论ID': [comment_id]})
        df = pd.concat([df, cache])
    return df


# 构造单集弹幕的循环网页，传入target_id和后缀ID(v_id)，通过设置爬取页数来改变timestamp的值完成翻页操作
def format_url(target_id, v_id, end=85):
    urls = []
    base_url = 'https://mfm.video.qq.com/danmu?otype=json&timestamp={}&target_id={}%26vid%3D{}&count=80&second_count=5'
    for num in range(15, end * 30 + 15, 30):
        url = base_url.format(num, target_id, v_id)
        urls.append(url)
    return urls


def get_all_ids(part1_url, part2_url, headers):
    # 分别获取1-30，31-46的所有后缀ID(v_id)
    part_1 = parse_base_info(part1_url, headers)
    part_2 = parse_base_info(part2_url, headers)
    df = pd.concat([part_1, part_2])
    df.sort_values('第几集', ascending=True, inplace=True)
    count = 1
    # 创建一个列表存储target_id
    info_lst = []
    # 循环获取后缀ID并传递
    for i in df['id']:
        # 得到每一集的后缀ID和target_ID
        info = get_episode_danmu(i, headers)
        info_lst.append(info)
        print('正在努力爬取第%d集的target_id' % count)
        count += 1
        time.sleep(2 + random.random())
    print('是不是发现多了一集，别担心，会去重的')
    # 根据后缀ID，将target_id和后缀ID所在的表合并
    info_lst = pd.DataFrame(info_lst)
    info_lst.columns = ['v_id', 'target_id']
    combine = pd.merge(df, info_lst, left_on='id', right_on='v_id', how='inner')
    # 去重复值
    combine = combine.loc[combine.duplicated('id') == False, :]
    return combine


# 输入包含v_id, target_id的表，并传入想要爬取多少集
def crawl_all(combine, num, page, headers):
    c = 1
    final_result = pd.DataFrame()
    for v_id, target_id in zip(combine['v_id'][:num], combine['target_id'][:num]):
        count = 1
        urls = format_url(target_id, v_id, page)
        for url in urls:
            result = parse_danmu(url, target_id, v_id, headers, c)
            final_result = pd.concat([final_result, result])
            time.sleep(2 + random.random())
            print('这是第%d集的第%d页爬取......' % (c, count))
            count += 1
        print('--------------------------------')
        c += 1
    return final_result


if __name__ == '__main__':
    # "都挺好"1-30集的网址，31-46集的网址
    # 如果要爬取其他电视剧，只需要根据文章的提示，找到存储后缀的ID的原网址即可
    part1_url = 'https://union.video.qq.com/fcgi-bin/data?otype=json&tid=682&appid=20001238&appkey=6c03bbe9658448a4&idlist=x003061htl5,t00306i1e62,x003061htl5,b0030velala,w0030ilim7z,i0030r7v63u,z003044noq2,m0030sfinyr,c0030u884k7,k0030m5zbr7,l0030e5nglm,h0030b060vn,j003090ci7w,n0030falyoi,s00308u9kwx,p0030fohijf,g00303ob0cx,v0030960y6n,x0030bl84xw,v0030keuav1,t0030kups1i,n0030y2o52i,x0030s52mev,d0030xuekgw,o0030md1a2a,x0030peo3sk,d00303l5j4k,t0030aexmnt,a0030ybi45z,y0030wpe2wu&callback=jQuery191020844423583354543_1554200358596&_=1554200358597'
    part2_url = 'https://union.video.qq.com/fcgi-bin/data?otype=json&tid=682&appid=20001238&appkey=6c03bbe9658448a4&idlist=t0030epjqsi,g003035mi84,n00301fxqbh,h0030zivlrq,d0030qc1yu2,m0030q9ywxj,h0030j0eq19,j0030jks835,a00308xw434,l0030tb319m,x0030xogl32,g0030fju3w3,a0030vrcww0,l0030jzi1mi,c0030mq8yjr,u00302fdo8v,a0030w9g57k,n0030wnj6i8,j0030h91ouj,j00304eu73n,t00305kc1f5,i0030x490o2,u0030jtmlj2,d003031ey5h,w0850w594k6,l0854pfn9lg,f08546r7l7a,d0854s0oq1z,m08546pcd9k,p0854r1nygj&callback=jQuery191020844423583354543_1554200358598&_=1554200358599'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    # 得到所有的后缀ID，基于后缀ID爬取target_id
    combine = get_all_ids(part1_url, part2_url, headers)

    # 设置要爬取多少集(num参数)，每一集爬取多少页弹幕(1-85页，page参数),这里默认是爬取第一集的5页弹幕
    # 比如想要爬取30集，每一集85页，num=30, page=85
    final_result = crawl_all(combine, num=1, page=5, headers=headers)
    # 保存为excel格式
    final_result.to_excel('都挺好弹幕.xlsx')





