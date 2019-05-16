import jieba
#jieba用来对中文分词
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

filename = 'postRecord.txt'
chtext = ''
with open(filename,encoding='utf8') as fin:
    lines = fin.readlines()
    for line in lines:
        line = line.strip('\n').split('\t')[3]
        chtext += ' '.join(jieba.cut(line,cut_all=True))
# 调用包PIL中的open方法，读取图片文件，通过numpy中的array方法生成数组
backgroud_Image = np.array(Image.open("back.png"))

 # 绘制词云图
wc = WordCloud(
    background_color='white',  # 设置背景颜色，与图片的背景色相关
    mask=backgroud_Image,  # 设置背景图片
    font_path='C:\Windows\Fonts\STZHONGS.TTF',  # 显示中文，可以更换字体
    max_words=40,  # 设置最大显示的字数
    stopwords={'xcar.com.cn','怎么','一个','还是','为什么','没有','就是','可以',
               '是不是','不是','今天','究竟','到底','没有','现在','大家',
               '哪里','那个','到底','同学','有人','有点','关于','一下',
               '有没有','问题','这个','你们','真的','如何','自己','还有','感觉','觉得','应该','这么','知道','那么'
        , '我们','不用','看到','哪个','什么','这种','这样','多少','啥子'
        , '出来','不要','今年','事情','需要','开始','不能'
        , '几个','最近','居然','已经','口','本','时候','情况','第一','各位','求助','看看','发现','注意','发生'
               ,'个人','不会','男子'},  # 设置停用词，停用词则不再词云图中表示
    max_font_size=150,  # 设置字体最大值
    random_state=6,  # 设置有多少种随机生成状态，即有多少种配色方案
    scale=1  # 设置生成的词云图的大小
)
# 传入需画词云图的文本
wc.generate(chtext)

image_colors = ImageColorGenerator(backgroud_Image)
plt.imshow(wc.recolor(color_func=image_colors))

# 隐藏图像坐标轴
plt.axis("off")
# 展示图片
plt.show()

# filename = "miao.txt"
# #聊天记录
# with open(filename,encoding='UTF-8') as f:
#     mytext = f.read()
# #打开文本
# mytext = " ".join(jieba.cut(mytext))
# photo_coloring = imread('2016.jpg')
# #词云背景图片白底
# wordcloud = WordCloud(background_color="white",font_path="simsun.ttf",max_words=200,mask=photo_coloring).generate(mytext)
# #中文注意下载simsun.ttf中文字体来替换
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")