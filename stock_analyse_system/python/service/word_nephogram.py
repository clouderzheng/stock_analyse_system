from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import path
import jieba

lj=path.dirname(__file__)   #当前文件路径
text=open(path.join(lj,r'C:\Users\root\Desktop\word.txt'),encoding='utf-8').read() #读取的文本
jieba.add_word('咬人猫')
jieba.add_word('喵酱')    #添加结巴分辨不了的词汇
jbText=' '.join(jieba.cut(text))
imgMask=np.array(Image.open(path.join(lj,r'C:\Users\root\Desktop\6597981261795990854.jpg')))   #读入背景图片
wc=WordCloud(
    background_color='white',
    max_words=500,
    font_path='msyh.ttc',    #默认不支持中文
    mask=imgMask,  #设置背景图片
    random_state=30 #生成多少种配色方案
).generate(jbText)
ImageColorGenerator(imgMask)   #根据图片生成词云颜色
plt.imshow(wc)
plt.axis('off')
plt.show()
# wc.to_file(path.join(lj,'biliDM.png'))
print('成功保存词云图片！')
