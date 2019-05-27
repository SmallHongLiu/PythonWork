import jieba
from wordcloud import WordCloud, STOPWORDS
from scipy.misc import imread  # 处理图像的函数
import matplotlib.pyplot as plt


text = 'paper   going   keep    fighting    happy   Backprogagation/BP  AI' \
       'technology  Chine   new     year    you     thanks  hha' \
       'hmmm    emmm    yesterday   sunday  Batch   Normalization/BN    Autoencoder' \
       'Algorithm   Approximation   Bias    Class-imbalance word hard' \
       'Clustering  Data mining     Data set    Deep Q-Learning Eigenvalue' \
       'decomposition'
# 对文本进行分词
cut_text = ''.join(jieba.cut(text))
# 读取图片
color_mask = imread('qiaoba.jpg')
# 生成词云
cloud = WordCloud(background_color="white",
                  mask=color_mask,
                  max_words=2000,
                  max_font_size=80)
word_cloud = cloud.generate(cut_text)

# 输出图片
plt.axis('off')
plt.imshow(word_cloud)
plt.show()