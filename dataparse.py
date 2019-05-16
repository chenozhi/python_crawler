import numpy as np
import pandas as pd
import chunk
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt


# # 选取等于某些值的行记录 用 ==
# df.loc[df['column_name'] == some_value]
#
# # 选取某列是否是某一类型的数值 用 isin
# df.loc[df['column_name'].isin(some_values)]
#
# # 多种条件的选取 用 &
# df.loc[(df['column'] == some_value) & df['other_column'].isin(some_values)]
#
# # 选取不等于某些值的行记录 用 ！=
# df.loc[df['column_name'] != some_value]
#
# # isin返回一系列的数值,如果要选择不符合这个条件的数值使用~
# df.loc[~df['column_name'].isin(some_values)]

# pandas有个专门把字符串转为时间格式的函数，to_datetime。第一个参数是原始数据，第二个参数是原始数据的格式
#df['trade_date'] = pd.to_datetime(df['trade_date'],format='%Y%m%d')

#读取文件
plt.style.use('classic')#设置经典样式
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
pd.set_option('expand_frame_repr', False)
def read_record():
    title = ["ID","日期","作者","标题","浏览","回复","链接"]
    df = pd.read_csv("postRecord.txt",sep='\t',names=title)
    #chunker = pd.read_csv("postRecord.txt",sep='\t',names=title,chunksize=1000)


    # 统计 作者 这一列中各个值出现的次数
    # tot = pd.Series([])
    # for piece in chunker:
    #     tot = tot.add(piece['作者'].value_counts(), fill_value=0)
    # new_tot = tot.sort_values(ascending=False)
    # print(new_tot[:10]
    #日期转换
    df['日期'] = pd.to_datetime(df['日期'], format='%Y-%m-%d')
    # 使用时间来进行索引
    df.set_index('日期', inplace=True)
    series = pd.Series([])
    jan = df['2019-01-01':'2019-01-31']
    dfFinal = pd.DataFrame(jan)
    feb = df['2019-02-01':'2019-02-28']
    dfFinal.append(feb)
    mar = df['2019-03-01':'2019-03-31']
    dfFinal.append(mar)
    april = df['2019-04-01':'2019-04-30']
    dfFinal.append(april)

    # dfNew = pd.DataFrame(series)
    # dfNew.plot.bar()
    data = {'Month': ['Jan', 'Feb', 'Mar', 'Apr'], 'Total':[len(jan),len(feb),len(mar),len(april)]}

    dfRe = pd.DataFrame(data)
    print(df['标题'])
    # dfRe.plot.bar(x='Month',y='Total')
    # plt.show()
    #df['日期'].plot()
    #df1 = df.loc[df['作者'].str.contains('白手帕')]
    #print(df.head(10))

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