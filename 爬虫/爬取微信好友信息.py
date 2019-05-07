import itchat
import numpy as np
import pandas as pd
from collections import defaultdict
import re
import jieba
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image as Image

# 参数hotReload＝True的目的是短时间内退出程序，再次登录可以不用扫码
itchat.auto_login(hotReload=True)
friends = itchat.get_friends(update=True)

# 获取自己的昵称
NickName = friends[0].NickName
# w为自己创建一个文件夹
os.mkdir(NickName)

# 刚刚创建的那个文件夹的相对路径
file = '/%s' % NickName
# 当前路径
cp = os.getcwd()
# 刚刚创建的那个文件夹的绝对路径
path = os.path.join(cp + file)
# 切换路径
os.chdir(path)

# 好友数量
number_of_friends = len(friends)
print(number_of_friends)

# pandas可以把数据处理成DataFrame
df_friends = pd.DataFrame(friends)

# 获取性别信息
Sex = df_friends.Sex

Sex_count = Sex.value_counts()

Province = df_friends.Province
Province_count = Province.value_counts()
# 有一些好友地理位置信息为空，过滤掉这一部分人
Province_count = Province_count[Province_count.index != '']

City = df_friends.City
City_count = City.value_counts()
# 有一些好友地理信息为空，过滤掉这一部分人
City_count = City_count[City_count.index != '']

file_name_all = NickName + '_basic_inf.txt'

write_file = open(file_name_all, 'w')

write_file.write(
    '你共有%d个好友,其中有%d个男生，%d个女生，%d未显示性别。\n\n' % (number_of_friends, Sex_count[1], Sex_count[2], Sex_count[0]) +
    '你的朋友主要来自省份：%s(%d)、%s(%d)和%s(%d)。\n\n' % (Province_count.index[0], Province_count[0],
    Province_count.index[1], Province_count[1], Province_count.index[2], Province_count[2]) +
    '主要来自这些城市：%s(%d)、%s(%d)、%s(%d)、%s(%d)、%s(%d)和%s(%d)。' % (City_count.index[0], City_count[0],
    City_count.index[1], City_count[1], City_count.index[2], City_count[2], City_count.index[3], City_count[3],
    City_count.index[4], City_count[4], City_count.index[5], City_count[5])
)

write_file.close()

'''分析好友签名'''
# 提取并清理签名，得到语料库
Signatures = df_friends.Signature
# 匹配表情
regex1 = re.compile('<span.*?</span>')
# 匹配两个以上占位符
regex2 = re.compile('\s{2,}')

# 用一个空格替换表情和多个空格
Signatures = [regex2.sub(' ', regex1.sub('', signature, re.S)) for signature in Signatures]
# 去除空字符串
Signatures = [signature for signature in Signatures if len(signature) > 0]

text = ' '.join(Signatures)

file_name = NickName + '_wechat_signatures.txt'

with open(file_name, 'w', encoding='utf-8') as f:
    f.write(text)
    f.close()

# jieba 分词分析语料库
word_list = jieba.cut(text, cut_all=True)

word_space_split = ' '.join(word_list)

# 画图，词云的背景和颜色
# coloring = np.array(Image.open('pic.png'))

# 生成词云
my_wordcloud = WordCloud(background_color='white',
                         max_words=2000,
                         # mask=coloring,
                         max_font_size=60,
                         random_state=42,
                         scale=2,
                         font_path='/simhei.ttf').generate(word_space_split)

file_name_p = NickName + '.jpg'
# 保存图片
my_wordcloud.to_file(file_name_p)

print('All down, over!')


