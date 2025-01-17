from numpy import *
import operator

def datingClassTest():
    """
    Desc:
        对约会网站的测试方法，并将分类错误的数量和分类错误率打印出来
    Args:
        None
    Returns:
        None
    """
    # 设置测试数据的的一个比例（训练数据集比例=1-hoRatio）
    hoRatio = 0.1  # 测试范围,一部分测试一部分作为样本
    # 从文件中加载数据
    datingDataMat, datingLabels = file2matrix("D:\\temp\\data-master\\机器学习\\2.KNN\\datingTestSet2.txt")  # load data setfrom file

    import matplotlib
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, 0], datingDataMat[:, 1], 15.0 * array(datingLabels), 15.0 * array(datingLabels))
    plt.show()

    # 归一化数据
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # m 表示数据的行数，即矩阵的第一维  1000
    m = normMat.shape[0]
    # 设置测试的样本数量， numTestVecs:m表示训练样本的数量
    numTestVecs = int(m * hoRatio)
    print('numTestVecs=', numTestVecs)
    errorCount = 0
    for i in range(numTestVecs):
        # 对数据测试
        classifierResult = classify0(normMat[i], normMat[numTestVecs : m], datingLabels[numTestVecs : m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        errorCount += classifierResult != datingLabels[i]
    print("the total error rate is: %f" % (errorCount / numTestVecs))
    print(errorCount)


def file2matrix(filename):
    """
    导入训练数据
    :param filename: 数据文件路径
    :return: 数据矩阵returnMat和对应的类别classLabelVector
    """
    fr = open(filename, 'r')
    # 获得文件中的数据行的行数
    numberOfLines = len(fr.readlines())
    # 生成对应的空矩阵
    # 例如: zeros(2，3)就是生成一个 2*3 的矩阵，各个位置上全是 0
    returnMat = zeros((numberOfLines, 3))  #prepare matrix to return
    # 类型 1,2,3# 不喜欢的人、魅力一般的人、极具魅力的人
    classLabelVector = []  # prepare labels return
    # 只读模式打开
    fr = open(filename, 'r')
    index = 0
    for line in fr.readlines():
        # str.strip([chars]) --返回移除字符串头尾指定的字符生成的新字符串
        line = line.strip()
        # 以 '\t' 切割字符串
        listFromLine = line.split('\t')
        # 每列的属性数据，即 features
        returnMat[index] = listFromLine[0 : 3]
        # 每列的类别数据，就是 label 标签数据
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    # 返回数据矩阵returnMat和对应的类别classLabelVector
    return returnMat, classLabelVector


def autoNorm(dataSet):
    """
    Desc:
        归一化特征值，消除属性之间量级不同导致的影响
    Args:
        dataSet -- 需要进行归一化处理的数据集
    Returns:
        normDataSet -- 归一化处理后得到的数据集
        ranges -- 归一化处理的范围
        minVals -- 最小值

    归一化公式:
        Y = (X-Xmin)/(Xmax-Xmin)
        其中的 min 和 max 分别是数据集中的最小特征值和最大特征值。该函数可以自动将数字特征值转化为0到1的区间。
    """
    # 计算每种属性的最大值、最小值、范围
    # A.min(0): 返回A每一列最小值组成的一维数组；
    # A.min(1)：返回A每一行最小值组成的一维数组；
    # A.max(0)：返回A每一列最大值组成的一维数组；
    # A.max(1)：返回A每一行最大值组成的一维数组；
    # 这里的0表示行，1
    # 表示列
    # minVals 是[0.       0.       0.001156]
    minVals = dataSet.min(0)
    # [9.1273000e+04 2.0919349e+01 1.6955170e+00]
    maxVals = dataSet.max(0)
    # 极差
    ranges = maxVals - minVals
    # -------第一种实现方式---start-------------------------
    # shape函数是numpy.core.fromnumeric中的函数，它的功能是读取矩阵的长度，比如shape[0]就是读取矩阵第一维度的长度
    # shape(dataSet)
    # 全部是0的 1000 * 3 矩阵------shape(dataSet)
    # 规范数据集
    normDataSet = zeros(shape(dataSet))
    # shape[0]就是读取矩阵第一维度的长度 1000
    m = dataSet.shape[0]
    # 生成与最小值之差组成的矩阵
    # tileNumpy的 tile() 函数，就是将原矩阵横向、纵向地复制。tile 是瓷砖的意思，顾名思义，这个函数就是把数组像瓷砖一样铺展开来 参考https://www.jianshu.com/p/9519f1984c70
    a = tile(minVals, (m, 1))
    # (m, 1) 结果是1000，求最大值?
    # tile(minVals, (m, 1))
    normDataSet = dataSet - tile(minVals, (m, 1))
    # 将最小值之差除以范围组成矩阵
    normDataSet = normDataSet / tile(ranges, (m, 1))  # element wise divide
    # -------第一种实现方式---end---------------------------------------------

    # # -------第二种实现方式---start---------------------------------------
    # norm_dataset = (dataset - minvalue) / ranges
    # # -------第二种实现方式---end---------------------------------------------
    return normDataSet, ranges, minVals


def classify0(inX, dataSet, labels, k):
    """
    Desc:
        kNN 的分类函数
    Args:
        inX -- 用于分类的输入向量/测试数据
        dataSet -- 训练数据集的 features
        labels -- 训练数据集的 labels
        k -- 选择最近邻的数目
    Returns:
        sortedClassCount[0][0] -- 输入向量的预测分类 labels

    注意: labels元素数目和dataSet行数相同；程序使用欧式距离公式.

    预测数据所在分类可在输入下列命令
    kNN.classify0([0,0], group, labels, 3)
    """

    # -----------实现 classify0() 方法的第一种方式----------------------------------------------------------------------------------------------------------------------------
    # 1. 距离计算
    dataSetSize = dataSet.shape[0]
    # tile生成和训练样本对应的矩阵，并与训练样本求差
    """
    tile: 列-3表示复制的行数， 行-1／2表示对inx的重复的次数

    In [8]: tile(inx, (3, 1))
    Out[8]:
    array([[1, 2, 3],
        [1, 2, 3],
        [1, 2, 3]])

    In [9]: tile(inx, (3, 2))
    Out[9]:
    array([[1, 2, 3, 1, 2, 3],
        [1, 2, 3, 1, 2, 3],
        [1, 2, 3, 1, 2, 3]])
    """
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    """
    欧氏距离:  点到点之间的距离
       第一行:  同一个点 到 dataSet 的第一个点的距离。
       第二行:  同一个点 到 dataSet 的第二个点的距离。
       ...
       第N行:  同一个点 到 dataSet 的第N个点的距离。

    [[1,2,3],[1,2,3]]-[[1,2,3],[1,2,0]]
    (A1-A2)^2+(B1-B2)^2+(c1-c2)^2
    """
    # 取平方
    sqDiffMat = diffMat ** 2
    # 将矩阵的每一行相加
    # .sum(axis = 0)是普通的相加，即对应列相加
    # 而当加入axis=1以后就是将一个矩阵的每一行向量相加 900* 3 变成 1* 900
    sqDistances = sqDiffMat.sum(axis=1)
    # 开方
    distances = sqDistances ** 0.5
    # 根据距离排序从小到大的排序，返回对应的索引位置
    # argsort() 是将x中的元素从小到大排列，提取其对应的index（索引），然后输出到y。
    # 例如: y=array([3,0,2,1,4,5]) 则，x[3]=1最小，所以y[0]=3;x[5]=5最大，所以y[5]=5。
    # print 'distances=', distances
    sortedDistIndicies = distances.argsort()
    # print 'distances.argsort()=', sortedDistIndicies

    # 2. 选择距离最小的k个点
    classCount = {}
    for i in range(k):
        # 找到该样本的类型
        voteIlabel = labels[sortedDistIndicies[i]]
        # 在字典中将该类型加一
        # 字典的get方法
        # 如: list.get(k,d) 其中 get相当于一条if...else...语句,参数k在字典中，字典将返回list[k];如果参数k不在字典中则返回参数d,如果K在字典中则返回k对应的value值
        # l = {5:2,3:4}
        # print l.get(3,0)返回的值是4；
        # Print l.get（1,0）返回值是0；
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # 3. 排序并返回出现最多的那个类型
    # 字典的 items() 方法，以列表返回可遍历的(键，值)元组数组。
    # 例如: dict = {'Name': 'Zara', 'Age': 7}   print "Value : %s" %  dict.items()   Value : [('Age', 7), ('Name', 'Zara')]
    # sorted 中的第2个参数 key=operator.itemgetter(1) 这个参数的意思是先比较第几个元素
    # 例如: a=[('b',2),('a',1),('c',0)]  b=sorted(a,key=operator.itemgetter(1)) >>>b=[('c',0),('a',1),('b',2)] 可以看到排序是按照后边的0,1,2进行排序的，而不是a,b,c
    # b=sorted(a,key=operator.itemgetter(0)) >>>b=[('a',1),('b',2),('c',0)] 这次比较的是前边的a,b,c而不是0,1,2
    # b=sorted(a,key=opertator.itemgetter(1,0)) >>>b=[('c',0),('a',1),('b',2)] 这个是先比较第2个元素，然后对第一个元素进行排序，形成多级排序。
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

    # ------------------------------------------------------------------------------------------------------------------------------------------
    # 实现 classify0() 方法的第二种方式

    # """
    # 1. 计算距离

    # 欧氏距离:  点到点之间的距离
    #    第一行:  同一个点 到 dataSet的第一个点的距离。
    #    第二行:  同一个点 到 dataSet的第二个点的距离。
    #    ...
    #    第N行:  同一个点 到 dataSet的第N个点的距离。

    # [[1,2,3],[1,2,3]]-[[1,2,3],[1,2,0]]
    # (A1-A2)^2+(B1-B2)^2+(c1-c2)^2

    # inx - dataset 使用了numpy broadcasting，见 https://docs.scipy.org/doc/numpy-1.13.0/user/basics.broadcasting.html
    # np.sum() 函数的使用见 https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.sum.html
    # """


#   dist = np.sum((inx - dataset)**2, axis=1)**0.5

# """
# 2. k个最近的标签

# 对距离排序使用numpy中的argsort函数， 见 https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.sort.html#numpy.sort
# 函数返回的是索引，因此取前k个索引使用[0 : k]
# 将这k个标签存在列表k_labels中
# """
# k_labels = [labels[index] for index in dist.argsort()[0 : k]]
# """
# 3. 出现次数最多的标签即为最终类别

# 使用collections.Counter可以统计各个标签的出现次数，most_common返回出现次数最多的标签tuple，例如[('lable1', 2)]，因此[0][0]可以取出标签值
# """
# label = Counter(k_labels).most_common(1)[0][0]
# return label

# ------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    datingClassTest()
