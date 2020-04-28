from sklearn.datasets import load_iris,fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Imputer
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
# li = load_iris()
#
# print("获取特征值")
# print(li.data)
# print("目标值")
# print(li.target)
# print(li.DESCR)

#注意返回值, 训练集 train  x_train, y_train        测试集  test   x_test, y_test
# x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25)
#
# print("训练集特征值和目标值：", x_train, y_train)
# print("测试集特征值和目标值：", x_test, y_test)

# news = fetch_20newsgroups(subset='all')
#
# print(news.data)
# print(news.target)
#

def knncls():
    """
    K-近邻预测用户签到位置
    :return:None
    """
    # 读取数据
    data = pd.read_csv("./data/FBlocation/train.csv")

    # 包括x，y坐标，accuracy：准确度：位置的偏差值，time：时间戳，place_id：目标值
    # print(data.head(10))

    # 处理数据
    # 1、缩小数据,查询数据查询，DataFrame中有个api为query 相当于查询的语句
    data = data.query("x > 1.0 &  x < 1.25 & y > 2.5 & y < 2.75")

    # 处理时间的数据
    time_value = pd.to_datetime(data['time'], unit='s')

    print(time_value)

    # 把日期格式转换成 字典格式 pd.DatetimeIndex
    time_value = pd.DatetimeIndex(time_value)

    # 构造一些特征
    data['day'] = time_value.day
    data['hour'] = time_value.hour
    data['weekday'] = time_value.weekday

    # 把时间戳特征删除
    data = data.drop(['time'], axis=1)

    print(data)

    # 把签到数量少于n个目标位置删除
    place_count = data.groupby('place_id').count()

    # reset_index可以使place_id由索引变成colunmn，索引变成计数0、1、2
    tf = place_count[place_count.row_id > 3].reset_index()

    data = data[data['place_id'].isin(tf.place_id)]

    # 取出数据当中的特征值和目标值
    y = data['place_id']

    x = data.drop(['place_id'], axis=1)

    # 进行数据的分割训练集合测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

    # 特征工程（标准化）
    std = StandardScaler()

    # 对测试集和训练集的特征值进行标准化
    x_train = std.fit_transform(x_train)

    x_test = std.transform(x_test)

    # 进行算法流程 # 超参数
    knn = KNeighborsClassifier()

    # # fit， predict,score
    # knn.fit(x_train, y_train)
    #
    # # 得出预测结果
    # y_predict = knn.predict(x_test)
    #
    # print("预测的目标签到位置为：", y_predict)
    #
    # # 得出准确率
    # print("预测的准确率:", knn.score(x_test, y_test))

def naviebayes():
    """
    朴素贝叶斯进行文本分类
    :return: None
    """
    news = fetch_20newsgroups(subset='all')

    # 进行数据分割
    x_train, x_test, y_train, y_test = train_test_split(news.data, news.target, test_size=0.25)

    # 对数据集进行特征抽取
    tf = TfidfVectorizer()

    # 以训练集当中的词的列表进行每篇文章重要性统计['a','b','c','d']
    x_train = tf.fit_transform(x_train)

    print(tf.get_feature_names())

    x_test = tf.transform(x_test)

    # 进行朴素贝叶斯算法的预测
    mlt = MultinomialNB(alpha=1.0)

    print(x_train.toarray())

    mlt.fit(x_train, y_train)

    y_predict = mlt.predict(x_test)

    print("预测的文章类别为：", y_predict)

    # 得出准确率
    print("准确率为：", mlt.score(x_test, y_test))

    # print("每个类别的精确率和召回率：", classification_report(y_test, y_predict, target_names=news.target_names))

    return None

if __name__ == '__main__':
    naviebayes() 