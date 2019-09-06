from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import path
import jieba
import os
import sina_service

def generate_word_nephogram(comment_txt_name):
    text=open(r'../../static/comment_picture/'+comment_txt_name,encoding='utf-8').read() #读取的文本
    jbText=' '.join(jieba.cut(text))
    imgMask = np.array(Image.open(path.join(r'../../static/comment_picture/word_background.jpg')))   #读入背景图片
    wc=WordCloud(
        background_color='white',
        max_words=500,
        font_path='msyh.ttc',    #默认不支持中文
        mask=imgMask,  #设置背景图片
        random_state=40 #生成多少种配色方案
    ).generate(jbText)
    ImageColorGenerator(imgMask)   #根据图片生成词云颜色
    # plt.imshow(wc)
    # plt.axis('off')
    # plt.show()
    """保存生成图片"""
    wc.to_file('../../static/comment_picture/'+comment_txt_name.split(".")[0]+".jpg")
    """删除评论文件"""
    os.remove(r'../../static/comment_picture/'+comment_txt_name)

    # print('成功保存词云图片！')

# generate_word_nephogram("comment.txt")

# print("comment.txt".split(".")[0])
