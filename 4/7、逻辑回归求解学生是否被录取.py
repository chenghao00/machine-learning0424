# 三大件
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

path = 'data' + os.sep + 'LogiReg_data.txt'
# 第一行是数据 故先设定为None 再指定它的列名names
pdData = pd.read_csv(path, header=None, names=['Exam 1', 'Exam 2', 'Admitted'])
print(pdData.head())
print(pdData.shape)

# 绘制散点图
positive = pdData[
    pdData['Admitted'] == 1]  # returns the subset of rows such Admitted = 1, i.e. the set of *positive* examples
negative = pdData[
    pdData['Admitted'] == 0]  # returns the subset of rows such Admitted = 0, i.e. the set of *negative* examples

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(positive['Exam 1'], positive['Exam 2'], s=30, c='b', marker='o', label='Admitted')
ax.scatter(negative['Exam 1'], negative['Exam 2'], s=30, c='r', marker='x', label='Not Admitted')
ax.legend()
ax.set_xlabel('Exam 1 Score')
ax.set_ylabel('Exam 2 Score')


# plt.show()

# 定义sigmoid函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 画图展示sigmoid函数
nums = np.arange(-10, 10, step=1)  # creates a vector containing 20 equally spaced values from -10 to 10
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(nums, sigmoid(nums), 'r')


# plt.show()


# 预测函数模块
# X为数据，theta为参数，np.dot()为矩阵乘法，将结果值传入sigmoid函数中
def model(X, theta):
    return sigmoid(np.dot(X, theta.T))


pdData.insert(0, 'Ones',
              1)  # in a try / except structure so as not to return an error if the block si executed several times
# set X (training data) and y (target variable)
orig_data = pdData.values  # convert the Pandas representation of the data to an array useful for further computations
print(orig_data.shape)
cols = orig_data.shape[1]
print(cols)
X = orig_data[:, 0:cols - 1]
print(X.shape)
y = orig_data[:, cols - 1:cols]

# convert to numpy arrays and initalize the parameter array theta
# X = np.matrix(X.values)
# y = np.matrix(data.iloc[:,3:4].values) #np.array(y.values)
theta = np.zeros([1, 3])
# print(X[:5],y[:5])
print(X[:5])
print(X.shape, y.shape, theta.shape)


# 损失函数
def cost(X, y, theta):
    left = np.multiply(-y, np.log(model(X, theta)))
    right = np.multiply(1 - y, np.log(1 - model(X, theta)))
    return np.sum(left - right) / (len(X))


print(cost(X, y, theta))


# 计算梯度
def gradient(X, y, theta):
    grad = np.zeros(theta.shape)
    error = (model(X, theta) - y).ravel()
    for j in range(len(theta.ravel())):  # for each parmeter
        term = np.multiply(error, X[:, j])
        grad[0, j] = np.sum(term) / len(X)
    return grad


##比较3种不同梯度下降方法
STOP_ITER = 0
STOP_COST = 1
STOP_GRAD = 2


def stopCriterion(type, value, threshold):
    if type == STOP_ITER:
        return value > threshold
    elif type == STOP_COST:
        return abs(value[-1] - value[-2]) < threshold
    elif type == STOP_GRAD:
        return np.linalg.norm(value) < threshold


import numpy.random


# 在做迭代更新前，先对数据进行洗牌
# 打乱数据洗牌
def shuffleData(data):
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols - 1]
    y = data[:, cols - 1:]
    return X, y


import time


def descent(data, theta, batchSize, stopType, thresh, alpha):
    # 梯度下降求解

    init_time = time.time()
    # 先对值进行初始化
    i = 0  # 迭代次数
    k = 0  # batch
    X, y = shuffleData(data)
    grad = np.zeros(theta.shape)  # 计算的梯度
    costs = [cost(X, y, theta)]  # 去计算损失值

    while True:
        # 先计算梯度，自定义一个梯度下降的方法，由batchsize控制，对应的数据的个数不一样
        grad = gradient(X[k:k + batchSize], y[k:k + batchSize], theta)
        k += batchSize  # 取batch数量个数据
        if k >= n:
            k = 0
            X, y = shuffleData(data)  # 重新洗牌
        theta = theta - alpha * grad  # 参数更新 进行梯度下降
        costs.append(cost(X, y, theta))  # 计算新的损失
        i += 1

        if stopType == STOP_ITER:
            value = i
        elif stopType == STOP_COST:
            value = costs
        elif stopType == STOP_GRAD:
            value = grad
        # 进行停止的判断
        if stopCriterion(stopType, value, thresh): break

    # 返回新的结果值
    return theta, i - 1, costs, grad, time.time() - init_time


# 画图显示 迭代多少次 停止策略，batch的结果
def runExpe(data, theta, batchSize, stopType, thresh, alpha):
    # import pdb; pdb.set_trace();
    # 梯度下降的获得结果，执行一次更新
    theta, iter, costs, grad, dur = descent(data, theta, batchSize, stopType, thresh, alpha)
    # 根据传的参数，选择梯度下降的方式以及停止策略，显示它的名字
    name = "Original" if (data[:, 1] > 2).sum() > 1 else "Scaled"
    name += " data - learning rate: {} - ".format(alpha)
    if batchSize == n:
        strDescType = "Gradient"
    elif batchSize == 1:
        strDescType = "Stochastic"
    else:
        strDescType = "Mini-batch ({})".format(batchSize)
    name += strDescType + " descent - Stop: "
    if stopType == STOP_ITER:
        strStop = "{} iterations".format(thresh)
    elif stopType == STOP_COST:
        strStop = "costs change < {}".format(thresh)
    else:
        strStop = "gradient norm < {}".format(thresh)
    name += strStop
    print("***{}\nTheta: {} - Iter: {} - Last cost: {:03.2f} - Duration: {:03.2f}s".format(
        name, theta, iter, costs[-1], dur))
    # 进行画图展示
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(np.arange(len(costs)), costs, 'r')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Cost')
    ax.set_title(name.upper() + ' - Error vs. Iteration')
    plt.show()
    return theta


# 不同的停止策略

# 选择的梯度下降方法是基于所有样本的
n = 100
### 设定迭代次数
runExpe(orig_data, theta, n, STOP_ITER, thresh=5000, alpha=0.000001)

### 根据损失值停止
runExpe(orig_data, theta, n, STOP_COST, thresh=0.000001, alpha=0.001)

### 根据梯度变化停止
runExpe(orig_data, theta, n, STOP_GRAD, thresh=0.05, alpha=0.001)

### 对比不同的梯度下降方法

# Stochastic descent  速度快，但稳定性差，需要很小的学习率
runExpe(orig_data, theta, 1, STOP_ITER, thresh=5000, alpha=0.001)
# 有点爆炸。。。很不稳定,把学习率调小一些
runExpe(orig_data, theta, 1, STOP_ITER, thresh=15000, alpha=0.000002)

# ### Mini-batch descent
runExpe(orig_data, theta, 16, STOP_ITER, thresh=15000, alpha=0.001)
# 结果 浮动仍然比较大，我们来尝试下对数据进行标准化 将数据按其属性(按列进行)减去其均值，
# 然后除以其方差。最后得到的结果是，对每个属性/每列来说所有数据都聚集在0附近，方差值为1
from sklearn import preprocessing as pp
from sklearn.preprocessing import StandardScaler

scaled_data = orig_data.copy()
scaled_data[:, 1:3] = pp.scale(orig_data[:, 1:3])
runExpe(scaled_data, theta, n, STOP_ITER, thresh=5000, alpha=0.001)

scaled_data2 = orig_data.copy()
std = StandardScaler()
scaled_data2[:, 1:3] = std.fit_transform(scaled_data2[:, 1:3])
runExpe(scaled_data2, theta, n, STOP_ITER, thresh=5000, alpha=0.001)

# 更多的迭代次数会使得损失下降的更多
runExpe(scaled_data, theta, n, STOP_GRAD, thresh=0.02, alpha=0.001)

# 随机梯度下降更快，但是我们需要迭代的次数也需要更多，所以还是用batch的比较合适！！！
runExpe(scaled_data, theta, 1, STOP_GRAD, thresh=0.002 / 5, alpha=0.001)

# 最优的方法
runExpe(scaled_data, theta, 16, STOP_GRAD, thresh=0.002 * 2, alpha=0.001)


# 精度
#设定阈值
def predict(X, theta):
    return [1 if x >= 0.5 else 0 for x in model(X, theta)]

scaled_X = scaled_data[:, :3]
y = scaled_data[:, 3]
predictions = predict(scaled_X, theta)
correct = [1 if ((a == 1 and b == 1) or (a == 0 and b == 0)) else 0 for (a, b) in zip(predictions, y)]
accuracy = (sum(map(int, correct)) % len(correct))
print ('accuracy = {0}%'.format(accuracy))
