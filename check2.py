if __name__ == "__main__":
    dataSet = loadDataSet()
    C1 = createC1(dataSet)
    minSupport = 0.8
    D = list(map(set,dataSet))
    L1,dataSupport = scanD(D,C1,minSupport)
    i = 0
    L = [L1]
    k = 2
    while (len(L[i]) > 0):
        Ck = aprioriGen(L[i], k)
        Lk, supK = scanD(D, Ck, minSupport)  # the number of elements is k which satisfied minsupport
        if (len(Lk) == 0):
            break;
        dataSupport.update(supK)
        L.append(Lk)
        k += 1
        i += 1
    rule = generateRules(L, dataSupport, minConference=0.5)


    def aprioriGen(Lk, k):
        retList = []
        retLen = len(Lk)
        for i in range(retLen):
            for j in range(i + 1, retLen):
                L1 = list(Lk[i])[:k - 2]
                L2 = list(Lk[j])[:k - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    retList.append(Lk[i] | Lk[j])
        return retList


    def scanD(D, Ck, minSupport):
        ssCnt = {}
        for item in D:
            for can in Ck:
                if can.issubset(item):
                    ssCnt[can] = ssCnt.get(can, 0) + 1
        numItem = len(list(D))
        retList = []
        supportData = {}
        if (numItem != 0):
            for key in ssCnt:
                support = ssCnt[key] / numItem
                if support >= minSupport:
                    retList.insert(0, key)
                    supportData[key] = support
        return retList, supportData


    newSet = []
    for conseq in H:
        # print(conseq)
        conf = supportData[subSet] / supportData[subSet - conseq]
        if conf >= minConference:
            brl.append((subSet - conseq, conseq, conf))
            newSet.append(conseq)

    m = len(H[0])
    # print(m, len(subSet))
    # 如果频繁项集中每项元素个数大于买m+1,即，可以分出m+1个元素在规则等式右边则执行
    if (len(subSet) > (m + 1)):
        # 利用函数aprioriGen生成包含m+1个元素的候选频繁项集后件
        Hm = aprioriGen(H, (m + 1))  # Hm is a set which  the length of each set in it is m+1
        # print(Hm,' ',len(Hm))
        # 如果AB->CD，AD->CB,不可以,那么 A—>CDB也一定是有的，所以这里就是一种小剪枝的操作，返回可信度高的那个。
        Hm = calculation(subSet, Hm, supportData, brl, minConference)
        # print(Hm,' ',len(Hm)),
        # 当候选后件集合中只有一个后件的可信度大于最小可信度，则结束递归创建规则
        if (len(Hm) > 1):
            splitForm(subSet, Hm, supportData, brl, minConference)

    length = len(H[0])
    # 说明允许subSet->H的操作
    if len(subSet) > (length + 1):
        Hm = aprioriGen(H, length + 1)
        # 如果AB->CD，AD->CB,不可以,那么 A—>CDB也一定是有的，所以这里就是一种小剪枝的操作，返回可信度高的那个。
        Hm = calculation(subSet, Hm, supportData, association, minConference)
        # 当候选后件集合中只有一个后件的可信度大于最小可信度，则结束递归创建规则
        if len(Hm) > 1:
            splitForm(subSet, Hm, supportData, association, minConference)

    association = []
    for i in range(1, len(L)):
        for subSet in L[i]:
            H1 = [frozenset([item]) for item in subSet]
            # print(H1)
            # 因为对于集合内的元素为3的来说，每两个都可以再组合成新的一个，所以对于大于3的要再组合
            if (i > 1):
                splitForm(subSet, H1, supportData, association, minConference)
            else:
                calculation(subSet, H1, supportData, association, minConference)