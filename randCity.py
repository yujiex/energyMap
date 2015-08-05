from Tkinter import *
import random as rd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scst

import util_loadData as ld
import util_array as ar
from util_time import *
import colorRamp as cl

master = Tk()
master.title("random city")
defaultbg = master.cget('bg')

# global settings
dim = 10    # city dimension
size = 30   # bd size
h_time = 20
density = 0.8
bdTypelist = ["Green", "FullServiceRestaurant", "Hospital",
              "LargeHotel", "LargeOffice", "MediumOffice",
              "MidriseApartment", "OutPatient", "PrimarySchool",
              "QuickServiceRestaurant", "SecondarySchool",
              "SmallHotel", "SmallOffice", "Stand-aloneRetail",
              "StripMall", "SuperMarket", "Warehouse"]

bdinitlist = ["", "FR", "HO", "LH", "LO", "MO", "MA", "OP", "PS", "QR",
              "SS", "SH", "SO", "SR", "SM", "SU", "WH"]
# get distribution:
def landequalLike():
    return [1.0/16] * (dim * dim)

# single use by some land
def landsingleUse(land):
    lst = [0.0] * 16
    lst[bdinitlist.index(land) - 1] = 1.0
    return lst

def landbyDis(distribution):
    a = scst.rv_discrete(values = (list(range(1, 17)), distribution))
    return a.rvs(size = (dim * dim))

category = 7

bd_font = "TkDefault 8 bold"
ot_font = "TkDefault 6"
font_color = "gray45"

# month is 0 indexing
hourList = range(8760)
hpermonth = 8760/12
seasons = [[0, 1, 11], [2, 3, 4], [5, 6, 7], [8, 9, 10]]
# loaddata
heatDict = ld.profile2Dict("energyData/meterData/", "Heating:Gas")
dfHeat = pd.DataFrame(heatDict)
coolDict = ld.profile2Dict("energyData/meterData/", "Cooling:Elec")
dfCool = pd.DataFrame(coolDict)
#print [[(x*hpermonth,(x + 1)*hpermonth) for x in y] for y in seasons]
dfHeatSeason = [[dfHeat[x*hpermonth:(x + 1)*hpermonth] 
                 for x in y] for y in seasons]
dfHeatSeason = [pd.concat(x) for x in dfHeatSeason]

dfCoolSeason = [[dfCool[x*hpermonth:(x + 1)*hpermonth] 
                 for x in y] for y in seasons]
dfCoolSeason = [pd.concat(x) for x in dfCoolSeason]

# functions for buttons
def advance24h():
    allyear.set(allyear.get() + 24)

def advance1h():
    allyear.set(allyear.get() + 1)

def back24h():
    allyear.set(allyear.get() - 24)

def back1h():
    allyear.set(allyear.get() - 1)

def showmsg():
    msgwindow = Tk()
    msgwindow.title("load balancing stats")
    defaultbg = master.cget('bg')

    heatmsg = Message(msgwindow,text = getmsg(dfHeatSeason, "Heating"),
                      font = bd_font, width = category * size, fg =
                      font_color)
    heatmsg.grid(row = 0, column = 0)
    coolmsg = Message(msgwindow,text = getmsg(dfCoolSeason, "Cooling"),
                      font = bd_font, width = category * size, fg =
                      font_color)
    coolmsg.grid(row = 0, column = 1)

def plotDay_heat():
    idx = allyear.get()
    f, axarr = plt.subplots(4, 4, sharex=True, sharey = True)
    for i in range(16):
        dfHeat.ix[idx: min(idx + 24, 8760), i].plot(ax=axarr[i/4, i%4], title = bdinitlist[i+1])
    plt.show()

def plotMonth():
    print "not implemented"

def plotSeason():
    print "not implemented"

def plotYear_heat():
    f, axarr = plt.subplots(4, 4)
    for i in range(16):
        dfHeat.ix[:, i].plot(ax=axarr[i/4, i%4])
    plt.show()

# create a starting board of random city
def createBoard(n_row, n_col, size, distribution):
    f_matrix = []
    l_matrix = []
    bd_cnt = [0] * 17
    landlist = landbyDis(distribution)
    for i in range(n_row):
        f_row = []
        l_row = []
        for j in range(n_col):
            f = Canvas(master, width = size, height = size)
            f.grid(row = i, column = j)
            f_row.append(f)

            landuse = 0
            color = "lawngreen"
            if (rd.random() < density):
                landuse = landlist[i * n_row + j]
                color = "red"
            bdtype = bdinitlist[landuse]
            bd_cnt[landuse] += 1

            f.create_rectangle(0, 0, size, size, fill = color, outline
                               = defaultbg)
            f.create_text(size/2, size/2, fill = font_color, font =
                          bd_font, text = bdtype)
            l_row.append(landuse)
        f_matrix.append(f_row)
        l_matrix.append(l_row)
    return (f_matrix, l_matrix, bd_cnt)

# used in main interface for creating 2d color ramp
def createColorScheme(cate, row_off, col_off, gridsize):
    for i in range(category):
        f = Canvas(master, width = gridsize, height = gridsize)
        f.grid(row = row_off, column = i + col_off + 1)
        f.create_text(2, gridsize, anchor = SW, font = ot_font, fill =
                      font_color, text =
                      str(int(round(heat_breakpt[i], 0))))
        g = Canvas(master, width = gridsize, height = gridsize)
        g.grid(row = i + row_off + 1, column = col_off)
        g.create_text(gridsize, 0, anchor = NE, font = ot_font, fill =
                      font_color, text =
                      str(int(round(cool_breakpt[i], 0))))

    zero_label = Canvas(master, width = gridsize, height = gridsize)
    zero_label.grid(row = 0, column = col_off)
    zero_label.create_text(gridsize/2, gridsize/2, text = "zero", font
                           = bd_font, fill = font_color)

    heat_label = Canvas(master, width = gridsize, height = gridsize)
    heat_label.grid(row = row_off, column = col_off + category + 1)
    heat_label.create_text(gridsize/2, gridsize/2, text = "heat", font
                           = bd_font, fill = font_color)
    heat_label.create_text(2, gridsize, anchor = SW, font = ot_font,
                           fill = font_color, text =
                           str(int(round(heat_breakpt[category], 0))))

    cool_label = Canvas(master, width = gridsize, height = gridsize)
    cool_label.grid(row = row_off + category + 1, column = col_off)
    cool_label.create_text(gridsize/2, gridsize/2, text = "cool", font
                           = bd_font, fill = font_color)
    cool_label.create_text(gridsize, 0, anchor = NE, font = ot_font,
                           fill = font_color, text =
                           str(int(round(cool_breakpt[category], 0))))

    f_color = []
    for i in range(cate):
        row_color = []
        for j in range(cate):
            f = Canvas(master, width = gridsize, height = gridsize)
            f.grid(row = i + row_off + 1, column = j + col_off + 1)
            f.create_rectangle(0, 0, gridsize, gridsize, fill =
                               colorGrid[i][j], outline = defaultbg)
            row_color.append(f)
        f_color.append(row_color)
    return f_color

# repaint 2d color ramp at the beginning of each time step
def repaintColor2d():
    for i in range(category):
        for j in range(category):
            f = color_2d[i][j]
            f.create_rectangle(0, 0, size, size, fill =
                               colorGrid[i][j], outline = defaultbg)

def changeColor(event):
    idx = allyear.get()
    (m, d, h) = hour2mdh(idx)
    time = mdh2str(m, d, h)
    time_label.create_rectangle(0, 0, w_slider, h_time, fill =
                                defaultbg, outline = defaultbg)
    time_label.create_text(w_slider/2, h_time/2, text = time,
                           font = bd_font, fill = font_color)
    repaintColor2d()
    for i in range(dim):
        for j in range(dim):
            landuse = l_2d[i][j]
            bdinit = bdinitlist[landuse]
            bdtype = bdTypelist[landuse]
            if landuse == 0:
                color = "lawngreen"
            else:
                heatid = heatColorDict[bdtype][idx]
                coolid = coolColorDict[bdtype][idx]
                color = colorGrid[coolid][heatid]
                g = color_2d[coolid][heatid]
                g.create_rectangle(0, 0, size, size,
                                   fill = colorGrid[coolid][heatid],
                                   outline = defaultbg)
                g.create_text(size/2, size/2, fill = font_color,
                              font = bd_font, text = "x")
            f = f_2d[i][j]
            f.create_rectangle(0, 0, size, size, fill = color, outline
                               = defaultbg)
            f.create_text(size/2, size/2, fill = font_color, font =
                          bd_font, text = bdinit)

#distribution = landequalLike()
distribution = landsingleUse("LH")
(f_2d, l_2d, bd_count) = createBoard(dim, dim, size, distribution)
countDict = dict(zip(bdTypelist, bd_count))
del countDict["Green"]

import itertools
headers = [x * [y] for (x, y) in zip(bd_count, bdTypelist) if y !=
           'Green']
headers = list(itertools.chain(*headers))

def generalMsg():
    bdtypemsg = ['{0:<5} {1:<5} {2:>5} : {3:<}'.format(n, round(p, 3), x, y) for (n, p, x, y) in zip(bd_count, distribution, bdinitlist, bdTypelist) if x != ""]
    bdtypemsg = "\n".join(bdtypemsg)
    densitymsg = "\n\nUrban Density: {0}\n\n".format(density)
    return (bdtypemsg + densitymsg)

def getmsg(dflist, cate):
    energy = ''
    season = ['winter', 'spring', 'summer', 'fall']
    count = 0
    for df in dflist:
        energy += (season[count]) + '\n'
        count += 1
        dfall = pd.DataFrame(df, columns = headers)
        dfall['total'] = dfall.sum(axis = 1)
        # total  demand max
        maxtotal = dfall['total'].max()
        mintotal = dfall['total'].min()
        dif = maxtotal - mintotal 
        ratio = round(float(dif)/maxtotal, 3)
        if cate == "Heating":
            energy += ('Max Heaing Demand (Gas)/kBtu: {0}\n'+
                       'Min Heaing Demand (Gas)/kBtu: {1}\n'+
                       'Heating Demand Variation/kBtu: {2}\n'+
                       'Heating Energy Variation Ratio: {3}\n\n').format(maxtotal, mintotal, dif, ratio)
        else:
            energy += ('Max Cooling Demand (Electricity)/kBtu: {0}\n'+
                       'Min Cooling Demand (Electricity)/kBtu: {1}\n'+
                       'Cooling Demand Variation/kBtu: {2}\n'+
                       'Cooling Energy Variation Ratio: {3}\n\n').format(maxtotal, mintotal, dif, ratio)
    return energy

# classify data
totalheat = ld.total_count(countDict, heatDict)
totalcool = ld.total_count(countDict, coolDict)
totalheat = [x for x in totalheat if x != 0.0]
totalcool = [x for x in totalcool if x != 0.0]
heat_breakpt = ld.breakpt(totalheat, category, "quantile", False)
cool_breakpt = ld.breakpt(totalcool, category, "quantile", False)

# create 2d colorRamp
colorGrid = cl.colorRamp_2d(category,[255, 255, 255],
                            [255, 0, 0], [0, 0, 255])
color_2d = createColorScheme(category, 0, dim, size)

heatColorDict = {}
for key in heatDict:
    if countDict[key] != 0:
        heatColorDict[key] = ar.bucket(heatDict[key], heat_breakpt)

coolColorDict = {}
for key in coolDict:
    if countDict[key] != 0:
        coolColorDict[key] = ar.bucket(coolDict[key], cool_breakpt)

# slider
row_time = max(dim, category + 2)
row_slider = row_time + 1
grid_horizontal = dim + category + 2
w_slider = grid_horizontal * size
allyear = Scale(master, from_= 0, length = w_slider, to = 8759,
                tickinterval=1000, orient=HORIZONTAL, command =
                changeColor, font = ot_font, fg = font_color)
allyear.set(0)
allyear.grid(row = row_slider, column = 0, columnspan =
             grid_horizontal )
monthTick = Canvas(master, width = w_slider, height = 15)
monthTick.grid(row = row_slider, column = 0, rowspan = 1,
               columnspan = grid_horizontal ,sticky = S)
monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
             "Sep", "Oct", "Nov", "Dec"]
for i in range(12):
    monthTick.create_line(1 + w_slider/12*i, 1, 1 + w_slider/12*i, 8,
                          fill = font_color)
    monthTick.create_text(w_slider/24 + w_slider/12*i, 7, text =
                          monthList[i], font = ot_font, fill =
                          font_color)

time_label = Canvas(master, width = w_slider, height = h_time)
time_label.grid(row = row_time, column = 0, columnspan =
                grid_horizontal)

row_button = row_slider + 1
w_button = 5
# create a row of buttons
buttonList = [{'text':'+24h', 'cmd':advance24h, 'col' : 0},
              {'text':'+1h', 'cmd':advance1h, 'col' : 2},
              {'text':'-24h', 'cmd':back24h, 'col' : 4},
              {'text':'-1h', 'cmd':back1h, 'col' : 6},
              {'text':'balance', 'cmd':showmsg, 'col' : 8},
              {'text':'heatyear', 'cmd':plotYear_heat, 'col' : 10},
              {'text':'heatday', 'cmd':plotDay_heat, 'col' : 12}]

for button in buttonList:
    f_button = Button(master, text = button['text'], command =
                      button['cmd'], width = w_button, font = bd_font,
                      fg = font_color)
    f_button.grid(row = row_button, column = button['col'], columnspan
                  = 2)

# display heating cooling msg
row_genmsg = 0
col_genmsg = dim + category + 2 
col_span_msg = 1
row_span_msg = dim 

genmsg = Message(master, text = generalMsg(), font = ot_font, width =
                 category * size, fg = font_color)
genmsg.grid(row = row_genmsg, column = col_genmsg, columnspan =
            col_span_msg, rowspan = row_span_msg)

#b_plotyear = Button(master, text = 'plot', command = plot_yr)
mainloop()
