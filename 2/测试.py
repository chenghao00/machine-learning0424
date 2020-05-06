import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
# 获取数据
titan = pd.read_csv("http://biostat.mc.vanderbilt.edu/wiki/pub/Main/DataSets/titanic.txt")

# 处理数据，找出特征值和目标值
x = titan[['pclass', 'age', 'sex']]

y = titan[['survived']]

#print(x)
# 缺失值处理
#x['age'].fillna(x['age'].mean(), inplace=True)

# 分割数据集到训练集合测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

# 进行处理（特征工程）特征-》类别-》one_hot编码
dict = DictVectorizer(sparse=False)

print(x_train.to_dict(orient="records"))