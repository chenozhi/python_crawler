import numpy as np
import pandas as pd
import chunk
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt

#读取文件
plt.style.use('classic')#设置经典样式
pd.set_option('display.max_columns',None)
pd.set_option('expand_frame_repr', False)
def read_record():
    title = ["ID","日期","作者","标题","浏览","回复","链接"]
    chunker = pd.read_csv("postRecord.txt",sep='\t',names=title,chunksize=1000)

    # 统计 作者 这一列中各个值出现的次数
    tot = pd.Series([])
    for piece in chunker:
        tot = tot.add(piece['作者'].value_counts(), fill_value=0)
    new_tot = tot.sort_values(ascending=False)
    print(new_tot[:10])



read_record()
#,link  as '链接'
# conn = sqlite3.connect('xcar.db')
# df = pd.read_sql_query("select postdate as '时间',author as '作者',title as '标题',link  as '链接' from april where author like '%object%'", conn)
# x = np.linspace(0, 10, 100)
#
# fig = plt.figure()
# plt.plot(x, np.sin(x), '-')
# plt.plot(x, np.cos(x), '--');
# plt.show()