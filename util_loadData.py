# in charge of aead simulation result in csv format, generate statistical plot
# create classify group to be used in creating colorRamp
# use -d to enter debug

# built-in librarys
import csv
import glob
import math

# my library function
import myString
import util_order as od
import util_array as ar

# python packages
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pylab as P  # fur save figure
from ggplot import *

def readLand():
    df = pd.read_csv("input/landusePattern2013.csv")
    #print df
    bdCountDict = dict(zip(df['Building Type'], df['Number']))
    bdTypeDict = dict(zip(df['Building Type'], df['TypeID']))
    areaDict = dict(zip(df['Building Type'], df['TotalArea']))
    initialDict = dict(zip(df['Building Type'], df['Initial']))
    bdSectorDict = dict(zip(df['Building Type'], df['Sector']))
    # get building type from file name
    bdFilenameDict= dict(zip(df['Filename'], df['Building Type']))
    return [bdCountDict, bdTypeDict, areaDict, initialDict,
            bdSectorDict, bdFilenameDict]
[bdCountDict, bdTypeDict, areaDict, initialDict, bdSectorDict, bdFilenameDict] = readLand()

# source:http://code.activestate.com/recipes/511478-finding-the-percentile-of-the-values/ of the following function
# this function is used for remove the dependency of numpy
def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1

# get the list of csv files, return the list of such files with dirName
# appended to the front
def getFileList(dirName):
    # list of input file
    filelist = []
    for (counter, files) in enumerate(glob.glob(dirName + "*.csv")):
        filelist.append(files)
#   if __debug__: print(filelist[0])
    return filelist

def test_getFileList():
    getFileList("energyData/meterData2013/")

# return building type associated with EnergyPlus simulation file:
# sample file name:
# RefBldgFullServiceRestaurantPost1980_v1.3_5.0_5A_USA_IL_CHICAGO-OHAREMeter.csv
def getBdType(filename):
#   return myString.midStr(filename, "RefBldg", "Post")
#   return myString.midStr(filename, "RefBldg", "New")
    infile = myString.midStr(filename, "_", "_")
    return bdFilenameDict[infile]

# read column of filename file with subHeader as a sub string of some Header
# return pair: (title, data), title = fun(filename)
# in this use case, the pair is (buildingType, energy profile)
# typeConvert is a function that converts string to desired type
def readCol2Pair(filename, subHeader, fun, typeConvert):
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)

        firstline = True
        data_col = -1
        counter = 0
        data = []
        for row in rows:
            if firstline:
                for item in row:
                    if (subHeader in item):
                        data_col = counter
                        break
                    counter += 1
                firstline = False
                if (data_col == -1):
                    print("no column with header: " + subHeader)
                    return ("", [])
                firstline = False
            else:
                data.append(typeConvert(row[data_col]))
    return (fun(filename), data)

# cols with subheaders are read to pair list, assume the order of
# subheaders appear in the same order as the full headers in the table
def readCols2Pair(filename, subHeaders, fun, typeConvert):
    num_col = len(subHeaders)
    with open(filename) as csvfile:
        rows = csv.reader(csvfile)

        firstline = True
        data_col = -1
        counter = 0
        data = []
        for row in rows:
            if firstline:
                for item in row:
                    if (subHeader in item):
                        data_col = counter
                    counter += 1
                firstline = False
                if (data_col == -1):
                    print("no column with header: " + subHeader)
                    return ("", [])
                firstline = False
            else:
                data.append(typeConvert(row[data_col]))
    return (fun(filename), data)

# to be feed in to typeConvert of function "readCol2Pair")
# convert J to kbtu with rounding
def j2kbtu(string):
    return (round(9.478e-7 * float(string), 1))

# get all energy profile of a category(subHeader) and output a
# dictionary with (key : building type, value : energyProfile)
def profile2Dict(dirName, subHeader):
    filelist = getFileList(dirName)
    pairList = []
    for item in filelist:
        pairList.append(readCol2Pair(item, subHeader, getBdType,
                                     j2kbtu))
    diction = dict(pairList)
    return diction

def test_profile2Dict():
    heatDict = profile2Dict("energyData/meterData2013/", "Heating:Gas")
    for key in heatDict:
        print '{0}:{1}'.format(key, heatDict[key][:10])

# #### #### #### #### #### #### #### #### #### #### ####
# Data Plot Generation
# #### #### #### #### #### #### #### #### #### #### ####

# plot energy profile with ggplot
def plotHistDictLine(key, diction, category, save_dir, uBound):
    df = pd.DataFrame(diction)
    p = ggplot(aes(x = 'time (hour)', y = key), data = df) + xlim(0, 8760) + ylim(0, uBound)
    p = p + geom_line()
    ggsave(plot = p, filename = "profile" + key + "-" + category + ".png", path = save_dir)

# plot energy profile with ggplot
def plotBoxDict(diction, save_name, label, title):
    df = pd.DataFrame(diction)
    df = df.rename(columns = initialDict)
    plt.figure()
    bp = df.boxplot()
    plt.ylabel(label)
    plt.title(title)
    P.savefig(save_name)
    plt.close()

def plotBar(diction, save_name, label, title):
    df = pd.DataFrame(diction)
    df.mean().to_csv('mean.csv')
    plt.figure()
    bp = df.mean().plot(kind='bar')
    plt.axhline(0, color='k')
    plt.ylabel(label)
    plt.title(title)
    P.savefig(save_name)
    plt.close()

def test_plotBar():
    heatDict = profile2Dict("energyData/meterData2013/", "Heating:Gas")
    coolDict = profile2Dict("energyData/meterData2013/", "Cooling:Elec")
    todel = []
    for key in heatDict:
        if bdCountDict[key] == 0:
            todel.append(key)
    for key in todel:
        del heatDict[key]
        del coolDict[key]
    label = "Heating(Gas)/kBtu"
    title = "Average Heating Demand Bar Plot"
    plotBar(heatDict, "mean/heatBar.png", label, title)
    '''
    label = "Cooling(Electricity)/kBtu"
    title = "Average Cooling Demand Bar Plot"
    plotBar(coolDict, "mean/coolBar.png", label, title)
    '''

# read the energy profiles to dictionaries of dictionary
# level 1 key is categories, level 2 key is building type
def read2dicts():
    dirdata = "energyData/meterData2013/"
    categories = ["Heating:Gas", "Heating:Electricity",
                  "Water Heater:WaterSystems:Gas",
                  "Water Heater:WaterSystems:Electricity",
                  "Cooling:Electricity", "Electricity:Facility"]
    dictArr = [profile2Dict(dirdata, x) for x in categories]
    dictSpaceHeat = {}
    for key in dictArr[0]:
        dictSpaceHeat[key] = [x + y for (x, y) in zip(dictArr[0][key],
                                                      dictArr[1][key])]
    dictHeat = {}
    for key in dictArr[0]:
        dictHeat[key] = [x + y + z + zz for (x, y, z, zz) in
                         zip(dictArr[0][key],dictArr[1][key],
                             dictArr[2][key], dictArr[3][key])]
    dictHE = {} # heat power ratio
    for key in dictArr[0]:
        dictHE[key] = [x / (y) for (x, y) in zip(dictHeat[key],
                                                 dictArr[5][key])]
    dictRecover = {}
    for key in dictArr[0]:
        if key == "LargeOffice" or key == "Hospital" or key == "HighriseApartment":
            dictRecover[key] = [x * 1.15 for x in dictArr[4][key]]
        else:
            dictRecover[key] = [x * 1.25 for x in dictArr[4][key]]
    dictWaterHeat = {}
    for key in dictArr[0]:
        dictWaterHeat[key] = [x + y for (x, y) in zip(dictArr[2][key],
                                                      dictArr[3][key])]

    dictArr.append(dictSpaceHeat)
    dictArr.append(dictHeat)
    dictArr.append(dictHE)
    dictArr.append(dictRecover)
    dictArr.append(dictWaterHeat)
    categories.append("Space Heating")
    categories.append("Heating")
    categories.append("Heating To Power Ratio")
    categories.append("Heat Recover")
    categories.append("Water Heating")
    return (categories, dictArr)

def test_plotBoxDict():
    (categories, dictArr) = read2dicts()
    labels = [x + "/kBtu" for x in categories]
    titles = [x + " Demand Box Plot" for x in categories]
    inits = ["".join([x for x in y if x.isupper()]) for y in categories]
    length = len(dictArr)
    for i in range(length):
        plotBoxDict(dictArr[i], "box/"+inits[i]+".png", labels[i], titles[i])

def plotHist(arr, category, save_dir):

    def space2Highfen(string):
        if ' ' in string:
            print('{0} has space\n'.format(string))
            strList = list(string)
            length = len(strList)
            for i in range(length):
                if strList[i] == ' ':
                    strList[i] = '-'
            return ''.join(strList)
        return string

    arr = [x for x in arr if x != 0]
    maxi = max(arr)
    col1 = 'original-'+space2Highfen(category)
#   col2 = 'linear-'+category
#   col3 = 'log-'+category
    col4 = 'log-Scale-'+space2Highfen(category)
    df = pd.DataFrame(pd.Series(arr), columns = [col1]) #original
#   df[col2] = (maxi - df[col1])/maxi
#   df[col3] = (np.log(maxi) - np.log(df[col1]))/np.log(maxi)
    df[col4] = np.log(df[col1])                         #logscale

    width = 6
    height = 5.5
    p1 = ggplot(aes(x = col1), data = df) + geom_histogram()
#   p2 = ggplot(aes(x = col2), data = df) + geom_histogram()
#   p3 = ggplot(aes(x = col3), data = df) + geom_histogram()
    p4 = ggplot(aes(x = col4), data = df) + geom_histogram()
    ggsave(plot = p1, filename = col1 + ".png", path = save_dir, width = width, height = height, dpi = 75) # reduce dpi to save compile time
#   ggsave(plot = p2, filename = col2 + "no0.png", path = save_dir)
#   ggsave(plot = p3, filename = col3 + "no0.png", path = save_dir)
#   ggsave(plot = p4, filename = col4 + ".png", path = save_dir, width = 5, height = 5, dpi = 100)
    ggsave(plot = p4, filename = col4 + ".png", path = save_dir, width = width, height = height, dpi = 75)

# two version of making plot
# use ggplot must use default binwidth, if changed the figure is weird
def plotHistDict(key, diction, category, save_dir):
    df = pd.DataFrame(diction)
    p = ggplot(aes(x = key), data = df)
    p = p + geom_histogram()
    ggsave(plot = p, filename = "profile" + key + "-" + category +
           ".png", path = save_dir)

'''
# use matplotlib to plot histogram
# category is the col subheader of the plotted data
def plotHistDict(key, diction, category, save_dir):
    plt.figure()
    plt.hist(diction[key], bins = 80, facecolor = "black")
    plt.ylabel("Frequency")
    plt.xlabel(category)
    plt.title(key)
    P.savefig(save_dir + key + "-" + category + ".png")
    plt.close()
'''
# return an array with num_building copies of profile for each
# building type e.g. If there are 3 hospitals in the model, 3 copies
# of hospital data point in the returned array
def total_count(cnt_dict, energy_dict):
    acc = []
    for key in cnt_dict:
        assert(key in energy_dict)
        acc = acc + cnt_dict[key] * energy_dict[key]
    return acc

def generalMsg():
    x = readLand()
    bd_count = x[0].values()
    area = x[2].values()
    bdinitlist = x[3].values()
    typelist = [key for key in x[3]]
    bdtypemsg = ['{0:<} : {1:<}'.format(x, y) for (x, y) in
                 zip(bdinitlist, typelist)]
    '''
    titlemsg = '{0:<7} {1:<} \n'.format("Count", "Area(sf)")
    bdtypemsg = ['{0:<7} {1:<}   {2:<} : {3:<}'.format(n, a, x, y) for
                 (n, a, x, y) in zip(bd_count, area, bdinitlist,
                                     typelist)]
    '''
    bdtypemsg = "\n".join(bdtypemsg)
#   return titlemsg + bdtypemsg
    return bdtypemsg

def test_generalMsg():
    print generalMsg()

def test_total_count():
    dict1 = {'a':1, 'b':2}
    dict2 = {'a':[3, 3], 'b':[5, 8]}
    assert(total_count(dict1, dict2) == [3, 3, 5, 8, 5, 8])
    dict1 = {'a':1, 'b':0}
    dict2 = {'a':[3, 3], 'b':[5, 8]}
    assert(total_count(dict1, dict2) == [3, 3])

def testPlot():
    heatDict = profile2Dict("energyData/meterData2013/", "Heating:Gas")
    maxheat = max(max(heatDict.values()))
    for key in heatDict:
        count = 0
        for item in heatDict[key]:
            if item == 0:
                count += 1
        print("number of 0 in" + key + " = " + str(count))
        plotHistDict(key, heatDict, "Heating:Gas", "test/Heat/")

def plotAll():
    # load data into dictionary
    # inefficient version

    (categories, dictArr) = read2dicts()
    '''
    idxlist = list(range(8760))
    heatDict['time (hour)'] = idxlist
    coolDict['time (hour)'] = idxlist
    '''
    '''
    # Heating
    for key in heatDict:
        if not (key == 'time (hour)'):
            # plot the profile Energy - time
            plotHistDictLine(key, heatDict, "Heating:Gas(kbtu)",
                             "line/Heat/", maxheat)
            # plot the histogram
            plotHistDict(key, heatDict, "Heating:Gas", "hist/Heat/")

    # Cooling
    for key in coolDict:
        if not (key == 'time (hour)'):
            plotHistDictLine(key, coolDict, "Cooling:Electricity(kbtu)",
                             "line/Cool/", maxcool)
            plotHistDict(key, coolDict, "Cooling:Electricity(kBtu)",
                         "hist/Cool/")

    '''
    # plot the total building energy distribution
    length = len(dictArr)
    for i in range(length):
        acc = total_count(bdCountDict, dictArr[i])
        plotHist(acc, categories[i], "hist/")

    '''
    acc = total_count(bdCountDict, heatDict)
    plotHist(acc, "Heating:Gas(kBtu)", "hist/")
    acc = total_count(bdCountDict, coolDict)
    plotHist(acc, "Cooling:Electricity(kBtu)", "hist/")
    '''

# classify "data" (list) into "num_category" groups using "method"
# wtnumpy: if with numpy, say True, otherwise say False
def breakpt(data, num_category, method, wtnumpy):
    minimaxi = od.findMinMax(data)
    mini = minimaxi[0]
    maxi = minimaxi[1]
    # equal distance of data between max and min
    if (method == "even"):
        breakpoints = ar.interp(mini, maxi, num_category + 1)
    # same number of data per group
    elif (method == "quantile"):
        interval = 1.0 / num_category * 100.0
        # if you have the numpy package
        if wtnumpy:
            breakpoints = [np.percentile(data, interval * x)
                           for x in range(num_category)] + [maxi + 1]
        else:
            interval = 1.0 / num_category
            breakpoints = [percentile(sorted(data), interval * x)
                           for x in range(num_category)] + [maxi + 1]
    # implement later
    elif (method == "Jenks"):
        print("not implemented yet!")
        # psudo code: Calculate the sum of squared deviations between
        # classes (SDBC).  Calculate the sum of squared deviations
        # from the array mean (SDAM).  Subtract the SDBC from the SDAM
        # (SDAM-SDBC). This equals the sum of the squared deviations
        # from the class means (SDCM).  After inspecting each of the
        # SDBC, a decision is made to move one unit from the class
        # with the largest SDBC toward the class with the lowest SDBC.
    return breakpoints

def test_breakpt():
    data = [5, 3, 2, 4, 1]
    print(breakpt(data, 5, "quantile", False))
    print(breakpt(data, 5, "quantile", True))

# classify "data" with "breakpoints"
def classify(data, breakpoints):
    return ar.bucket(data, breakpoints)

# replace with previous implementation later on
def rawReadCol(dirname, subHeaderList, outputname):
    fileList = getFileList(dirname)
    with open (dirname + outputname + ".csv", "a") as wt:
        mywriter = csv.writer(wt, delimiter=",")
        for filename in fileList:
            landuse = bdTypeDict[getBdType(filename)]
            with open(filename) as csvfile:
                rows = csv.reader(csvfile)

                firstline = True
                data_col = []
                counter = 0

                for row in rows:
                    if firstline:
                        for item in row:
                            for hd in subHeaderList:
                                if (hd in item):
                                    data_col.append(counter)
                            counter += 1
                        firstline = False
                        if (len(data_col) == 0):
                            print("no column with header: " + subHeader)
                            return
                        firstline = False
                    else:
                        mywriter.writerow([row[x] for x in data_col] + [landuse])

def cvtTime(string):
    return string

def cvt(stringList):
    length = len(stringList)
    output = []
    output.append(cvtTime(stringList[0]))
    for i in range(1, length - 1):
        output.append(j2kbtu(stringList[i]))
    output.append(stringList[length - 1])
    return output

def convertData(dirname, inputname, outputname):
    with open (dirname + outputname + ".csv", "a") as wt:
        mywriter = csv.writer(wt, delimiter=",")
        with open(dirname + inputname + ".csv") as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                mywriter.writerow(cvt(row))

def testClassify():
    testArrays = []
    arr = list(range(20, 100))
    testArrays.append(arr)
    arr = [x**2 for x in range(100)]
    testArrays.append(arr)
    arr = [x**3 for x in range(100)]
    testArrays.append(arr)
    arr = [math.log(x + 1) for x in range(100)]
    testArrays.append(arr)
    heatDict = profile2Dict("energyData/meterData2013/", "Heating:Gas")
    arr = heatDict["LargeHotel"][:100]
    testArrays.append(arr)

    for arr in testArrays:
        print("arr is:")
        print(arr)
        bp = breakpt(arr, 3, "even", True)
        arr_even = classify(arr, bp)
        print 'even break point: {0}'.format(bp)
        bp = breakpt(arr, 3, "quantile", True)
        print 'quantile break point: {0}'.format(bp)
        arr_quan = classify(arr, bp)
        for i in range(3):
            print("# of %d:" % i)
            print(arr_even.count(i))
            print("# of %d:" % i)
            print(arr_quan.count(i))

# generate input for ArcScene model
def formatGIS():
    rawReadCol("energyData/meterData2/",
               ["Date/Time", "Heating:Gas", "Cooling:Elec"], "output")
    convertData("energyData/meterData2/", "output", "output2")

# write to csv files of energy profile
# used in dynamic data plot in main interface
def writeSector(dirname):
    sectorList = ["Hotel", "Office", "Residencial", "Commercial"]
    # category are "Heating:Gas" or "Cooling:Elec"
    (categories, dictArr) = read2dicts()

    suffixs = ["_h_gas", "_h_elec", "_water_gas", "_water_elec", "_c_elec",
               "_elec", "_spaceheat", "_heat", "_h2p", "_recov", "_water"]

    length = len(categories)
    for i in range(length):
        diction = dictArr[i]
        for sector in sectorList:
            filename = dirname + sector + suffixs[i] + ".csv"
            with open (filename, "w") as wt:
                mywriter = csv.writer(wt, delimiter=",")
                bdList = [] # building types in the sector
                for key in diction:
                    if (sector == bdSectorDict[key]):
                        bdList.append(key)
                # element in result list = diction[bd] * bdCountDict[bd]
                energylist = [diction[x] for x in bdList]
                countlist = [bdCountDict[x] for x in bdList]
                row = ar.scaleSum(energylist, countlist)
                mywriter.writerow(row)
        energylist = []
        countlist = []
        for key in diction:
            energylist.append(diction[key])
            countlist.append(bdCountDict[key])
        filename = dirname + "Community" + suffixs[i] + ".csv"
        with open(filename, "w") as wt:
            mywriter = csv.writer(wt, delimiter=",")
            row = ar.scaleSum(energylist, countlist)
            mywriter.writerow(row)

def main():
#   testPlot()
#   plotAll()
#   testClassify()
#   writeSector("energyData/")
#   test_total_count()
#   test_breakpt()
#   test_plotBoxDict()
#   test_plotBar()
#   test_generalMsg()
#   test_profile2Dict()
    return 0

main()
