from pandas.io.json import json_normalize
import pandas as pd
import requests
import json

import jieba.analyse
import os
from pyecharts.charts import WordCloud
from pyecharts.globals import SymbolType, ThemeType
from pyecharts.charts import Page
from pyecharts import options as opts

def get_comment_word(df):
    # 集合形式存储-去重
    stop_words = set()
    print(stop_words)

    # 加载停用词
    cwd = os.getcwd()
    stop_words_path = cwd + '/stop_words.txt'
    print(stop_words_path)

    with open(stop_words_path, 'r', encoding="ISO-8859-1") as sw:
        for line in sw.readlines():
            stop_words.add(line.strip())
    print(stop_words)

    # 合并评论信息
    df_comment_all = df['content'].str.cat()

    # 使用TF-IDF算法提取关键词
    word_num = jieba.analyse.extract_tags(df_comment_all, topK=300, withWeight=True, allowPOS=())
    print(word_num)
    # 做一步筛选
    word_num_selected = []

    # 筛选掉停用词
    for i in word_num:
        if i[0] not in stop_words:
            word_num_selected.append(i)
        else:
            pass

    return word_num_selected

def parse(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    data = requests.get(url, headers=headers)
    data = json.loads(data.text)
    results = data['comments'].values()
    s = json_normalize(results)
    #print(s, type(df))
    return s

if __name__ == '__main__':
    # url_list = [
    #     "http://comment.api.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/FASTLQ7I00038FO9/comments/newList?ibc=newspc&limit=30&showLevelThreshold=72&headLimit=1&tailLimit=2&offset={}".format(
    #         str(i * 30)) for i in range(30)]
    # df = pd.DataFrame(None)
    # for url in url_list:
    #     results = parse(url)
    #     df = df.append(results)
    # df.to_csv('data.csv')

    # todo：数据预处理
    # 数据读取
    df1 = pd.read_csv('data.csv')
    # 评论去重
    df1 = df1.drop_duplicates('commentId').reset_index(drop=True)
    # 格式转换
    df1['new_time'] = df1.apply(lambda x: x['createTime'].split(':', 1)[0], axis=1)


    # 对df1进行可视化处理
    word_num_selected=get_comment_word(df1)

    worldcloud = (
    WordCloud().add("", word_num_selected, word_size_range=[10, 100], shape=SymbolType.DIAMOND).set_global_opts(title_opts=opts.TitleOpts(title="小罗志祥词云"))
       )

    worldcloud.render('word.html')