#首先扫描一次数据库得到所有1个元素的频繁集
#获得长度为k+1的候选数据从长度为k的频繁集元素中
#当不再有频繁集可以被生成时停止
#List添加在末尾append()
#set 添加在末尾add()
#如果要判断一个元素是否在一些不同的条件内符合use set is better
import datetime
import sys
def loadDataSet():
     dataSet= [line.split() for line in open('homework1.dat').readlines()]
     return dataSet

#因为要将C1作为键值来使用
#最后之所以要先变为set再成list是为了后面的内部查询。
def find1Item(dataSet):
    C1 = []
    for transaction in dataSet:
        for idx in transaction:
            if [idx] not in C1:
                C1.append([idx])
    return list(C1)
    # return list(map(frozenset,C1))

#字典(Dictionary) get() 函数返回指定键的值，如果值不在字典中返回默认值。
#D是整个数据集，Ck是包含K个元素的数据集
#返回resList 是满足最小支持度的数据集
#该函数是对数据集的一次筛选，返回满足支持度的数据
def scanD(D, Ck, minSupport):
    count = {}
    for item in D:
        for key in Ck:
            if key.issubset(item):
                count[key] = count.get(key, 0) + 1#在这里为了提升最后的运行速度改为了字典序查询
    number = len(list(D))
    # print(number)
    resList = []
    supportData = {}
    supportNumber ={}
    if (number != 0):
        for key in count:
            support = count[key] / number
            suppotnumber = count[key]
            if support >= minSupport:
                resList.insert(0, key)
                supportData[key] = support
                supportNumber[key] = suppotnumber
    #   print (resList,supportData)
    return resList, supportData, supportNumber

#从K开始，通过前面的k-1个数，获得k+1个数
def apriori_gen(Lk, k):
    Ck = []
    resLen = len(Lk)
    for i in range(resLen):
        for j in range(i + 1, resLen):
            #这里的切片是切出前k-1个元素
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                c = Lk[i] | Lk[j]
                # if not hasInfresSub(c, Lk):
                Ck.append(c)
                # resList.append(Lk[i][:k-2])
                # resList.append(Lk[i][k-2])
                # resList.append(Lk[j][k-2])
    return Ck
# Lk是原来的k个元素，Ck是K+1个元素，要看是否k+1个元素的子集都在Lk中
# def hasInfresSub(c,Lk):
#     nc = set(c)
#     for key in c:
#         if not (nc-set(key)).issubset(Lk):
#             return True
#     return False
def associationRules(L,supportData,minConference):
    association = []
    for i in range(1, len(L)):
        for subSet in L[i]:
            H = [set([item]) for item in subSet]
            # print(H)
            # 因为对于集合内的元素为3的来说，每两个都可以再组合成新的一个，所以对于大于3的要再组合
            # if (i == 1):
            # else:
            splitForm(subSet, H, supportData, association, minConference)
    return association

#subSet频繁集中，每一个频繁集，H频繁集内每一个数字的拆分。
#合起来是频繁集，那么分开来一定也在频繁集里
def calculation(subSet, H, supportData,association,minConference):
    newSet = []
    for idx in H:
       confident = supportData[subSet]/supportData[subSet - idx]#说明subset-idx ->idx
       if confident >= minConference:
           association.append((subSet-idx,"-->",idx,confident))
           newSet.append(idx)
    return newSet

#对于元素个数大于2的说明里面的每一个都可以再两两组合，所以要再生成大的放入再求置信度。
def splitForm(subSet, H, supportData, association, minConference):
    length = len(H[0])
    # 说明允许subSet->H的操作
    if len(subSet) > (length + 1):
        Hk = apriori_gen(H, length + 1)
        # 如果AB->CD，AD->CB,不可以,那么 A—>CDB也一定是有的，所以这里就是一种小剪枝的操作，返回可信度高的那个。
        Hk = calculation(subSet, Hk, supportData, association, minConference)
        # 当可以合并的元素少于2时，就不进行再拆分合并，结束递归
        if len(Hk) > 1:
            splitForm(subSet, Hk, supportData, association, minConference)
    else:
        calculation(subSet, H, supportData, association, minConference)

#map()函数，会根据前面一共的函数对指定序列做映射
#把dataset映射成为Set
#首先生成C1，即集合元素为1的集合
#接着从C1开始生成，其集合元素为K的,再不断的进行剪枝，合并操作。
def apriori(dataset,minSupport):
    C1 = list(map(frozenset,find1Item(dataset)))
    D = list(map(set, dataset))
    L1, supportData ,supportNumber= scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    i = 0
    while (len(L[i]) > 0):
        Ck = apriori_gen(L[i], k)
        Lk, sup ,supportN= scanD(D, Ck, minSupport)
        if len(Lk) == 0:#当长度为0时停止操作
            break;
        supportData.update(sup)#这里保留这些数据是为了后面的关联规则挖掘用。
        supportNumber.update(supportN)
        L.append(Lk)
        k += 1
        i += 1
    return L,supportData,supportNumber
if __name__ == "__main__":
    dataset = loadDataSet()
    minSupport = float(sys.argv[1])
    minconf = float(sys.argv[2])
    frequentfile = sys.argv[3]
    rulefile = sys.argv[4]
    starttime = datetime.datetime.now()
    L,supportData ,supportNumber = apriori(dataset,minSupport)
    # print(supportNumber)
    endtime = datetime.datetime.now()
    print("寻找频繁集的运行时间为：",(endtime-starttime).seconds)
    starttime = datetime.datetime.now()
    R = associationRules(L, supportData,minconf)
    endtime = datetime.datetime.now()
    print("挖掘关联规则的运行时间为:",(endtime-starttime).seconds)
    f1 = open(frequentfile, 'w')


    for item , key in supportNumber.items():
        f1.write(str({key,item}))
        f1.write("\n")
    f1.close()

    f2 = open(rulefile, 'w')
    for item in R:
        f2.write(str(item))
        f2.write("\n")
    f2.close()

