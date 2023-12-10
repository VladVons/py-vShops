'''
python lesson.
loop speed test 
2022.01.29

Output:
Method: Test_01, Time: 0.33, Found: 6
Method: Test_03, Time: 0.11, Found: 6
Method: Test_04, Time: 0.04, Found: 6
'''

import time


def Test_01(aArr, aFind):
    Res = 0
    i = 0
    while(i < len(aArr)):
        if (aArr[i] == aFind):
            Res += 1
        i += 1
    return Res

def Test_02(aArr, aFind):
    #Arr = [i for i, a in enumerate(Arr1) if a == aFind]
    Arr = [a for a in Arr1 if a == aFind]
    return len(Arr)

def Test_03(aArr, aFind):
    Res = 0
    for a in aArr:
        if (a == aFind):
            Res += 1
    return Res

def Test_04(aArr, aFind):
    Res = aArr.count(aFind)
    return Res

#---
def SpeedFunc(aFunc, aArr, aFind, aCount):
    Start = time.time()
    for a in range(aCount):
        Res = aFunc(aArr, aFind)
    print('Method: %s, Time: %0.2f, Found: %d' % (aFunc.__name__, time.time() - Start, Res))

def SpeedAll(aArr, aFind, aCount):
    print()
    Methods = [Test_01,Test_02,  Test_03, Test_04]
    for Method in Methods:
        SpeedFunc(Method, aArr, aFind, aCount)

#---
def DTimer(aFunc):
    def Decor(aArr, aFind):
        Start = time.time()
        Count = 1 * 1000000
        for a in range(Count):
            Res = aFunc(aArr, aFind)
        print('Method: %s, Time: %0.2f, Found: %s' % (aFunc.__name__, time.time() - Start, Res))
    return Decor

@DTimer
def Test_04_Decor(aArr, aFind):
    Test_03(aArr, aFind)


#---
Arr1 = [2, 3, 7, 1, 5, 3, 12, 18, 3, 4, 3, 1, 16, 9, 7, 3, 3]

SpeedAll(Arr1, 3, 1*1000000)
#Test_04_Decor(Arr1, 3)
