import util_array as ar
import util_order as od
# number of days for each month in a non-leap year
numdays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

import numpy
from random import randint

def findInterval(item, lst):
    return od.lisearch(lst, item, "ceil")

def mdh2str(month, date, hour):
    date = min(numdays[month - 1], date)
    return ('2015/' + str(month) + '/' + str(date) + '    ' +
            str(hour) + ':00:00')

def hour2mdh(hour):
    day = hour // 24 + 1
    hour = hour % 24
    lst = ar.prefixSum(numdays)
    idx = findInterval(day, lst)
    month = 1 + idx
    if idx == 0:
        date = day
    else:
        date = day - lst[idx - 1]
    return [month, date, hour]

# turn imgxxxx.gif to hour index as int
def imgName2hour(name):
    digitList = [int(name[6]), int(name[5]), int(name[4]),
                 int(name[3])]
    powerList = []
    for i in range(4):
        powerList.append(digitList[i] * 10**i)
    print(powerList)
    return sum(powerList)

# turn integer value hour (restricted to 4 digit) to image name
# make the path directory be images/imgxxxx.gif
def hour2imgName(hour, dim):
#   dirname = 'images/'  # snapshot round one
#   dirname = 'imagesRedBlue/'
    dirname = 'images2d/'
    if (dim == "3D"):
        dirname = 'imagesRedBlue/'
    if hour < 10:
        return dirname + 'img000' + str(hour) + '.gif'
    elif hour < 100:
        return dirname + 'img00' + str(hour) + '.gif'
    elif hour < 1000:
        return dirname + 'img0' + str(hour) + '.gif'
    else:
        return dirname + 'img' + str(hour) + '.gif'

# check if month \in [0, 11] with 0 indexing
def isValidMonth(month):
    if (month < 0 or month > 11):
        print("Invalid Month!")
        return 0
    else:
        return 1

# check if month \in [0, 23] with 0 indexing
def isValidHour(hour):
    return ((0 <= hour) and (hour < 24))

def test_isValidHour():
    assert (isValidHour(0))
    assert (isValidHour(10))
    assert (isValidHour(23))
    assert (not isValidHour(24))
    assert (not isValidHour(-1))
    print("All test passed!!")

# check if (month, data) is a valid date
def isValidDate(month, date, datelist):
    if (len(datelist) != 12):
        print("invalid datelist length")
        return False
    elif (not isValidMonth(month)):
        print("month out of range")
        return False
    return ((date > 0) and (date <= datelist[month]))

def test_isValidDate():
    assert (isValidDate(0, 1, numdays))
    assert (isValidDate(0, 10, numdays))
    assert (isValidDate(0, 31, numdays))
    assert (not isValidDate(0, 32, numdays))
    assert (isValidDate(1, 1, numdays))
    assert (isValidDate(1, 10, numdays))
    assert (isValidDate(1, 28, numdays))
    assert (not isValidDate(1, 30, numdays))
    assert (isValidDate(6, 1, numdays))
    assert (isValidDate(11, 1, numdays))
    assert (isValidDate(11, 31, numdays))
    assert (not isValidDate(11, 32, numdays))
    # out of range test
    assert (not isValidDate(12, 1, numdays))

# round date to correct number of days in a month (because slider need
# to account for upper bound of month, month is 0 index
def roundDate(month, date, datelist):
    u_bound = datelist[month]
    return min(date, u_bound)

def test_roundDate():
    assert (roundDate(0, 1, numdays) == 1)
    assert (roundDate(0, 32, numdays) == 31)
    assert (roundDate(1, 1, numdays) == 1)
    assert (roundDate(1, 29, numdays) == 28)
    print("All test passed!!")

# input month is 1 index
def mdh2hour(month, date, hour, monthlist):
    month_idx = month - 1
    date = roundDate(month_idx, date, monthlist)
    # checks
    if (not isValidMonth(month_idx)):
        print("invalid month")
        return -1
    if (not isValidDate(month_idx, date, monthlist)):
        print("invalid date")
        return -1
    if (not isValidHour(hour)):
        print("invalid hour")
        return - 1
    # prefix sum of months
    sumDays = [0] + ar.prefixSum(monthlist)[0:11]
    result = ((sumDays[month_idx] + (date - 1)) * 24 + hour)
    return result

def test_mdh2hour():
    # need to import csv for testing
    timeTable = numpy.loadtxt("timeTest.txt", delimiter = ',',
                              dtype = 'int')
    # [idx, hour, day, month]
    i = randint(0, 8759)
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    i = randint(0, 8759)
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    i = randint(0, 8759)
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    i = randint(0, 8759)
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    i = 0
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    i = 8759
    if (mdh2hour(timeTable[i][3], timeTable[i][2],
        timeTable[i][1], numdays) != timeTable[i][0]):
        print("wrong hour" + str(i))
    print("All test passed!!")

# converting the triple of month-day-hour to hour
def time2hour(month, date, hour):
    lst = ar.prefixSum(numdays)
    if month == 1:
        return (date - 1) * 24 + hour
    return (lst[month - 2] + date - 1) * 24 + hour

def test_time2hour():
    print('time2hour(1, 1, 0)')
    print(time2hour(1, 1, 0))
    print('time2hour(1, 1, 23)')
    print(time2hour(1, 1, 23))
    print('time2hour(1, 15, 23)')
    print(time2hour(1, 15, 23))
    print('time2hour(1, 15, 10)')
    print(time2hour(1, 15, 10))
    print('time2hour(2, 1, 0)')
    print(time2hour(2, 1, 0))
    print('time2hour(3, 1, 23)')
    print(time2hour(3, 1, 23))
    print('time2hour(12, 31, 0)')
    print(time2hour(12, 31, 0))
    print('time2hour(12, 31, 23)')
    print(time2hour(12, 31, 23))

def test_findInterval():
    assert (0 == findInterval(1, lst))
    assert (0 == findInterval(10, lst))
    assert (0 == findInterval(31, lst))
    assert (1 == findInterval(32, lst))
    assert (1 == findInterval(45, lst))
    assert (11 == findInterval(365, lst))
    assert (-1 == findInterval(366, lst))
    print("all test passed!")
# main()
