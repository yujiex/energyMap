from Tkinter import *
#from time import sleep
import csv
import ast
from util_time import *
import plotGraph
import util_loadData as ld
import colorRamp as cr
import util_geo as geo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ggplot import *
import util_array as ar

# ###############
# global setting of user interface
w_photo = plotGraph.w_photo
h_photo = plotGraph.h_photo
photo_tb = plotGraph.photo_tb
photo_lr = plotGraph.photo_lr
w_window = plotGraph.w_window
h_window = plotGraph.h_window
h_slider = plotGraph.h_slider
w_graph = plotGraph.graph_width
h_graph = plotGraph.graph_height

h_slider = 10
w_slider = w_window
w_button = 3
w_ckbutton = 2
w_scale = 10

category = 7
w_span_colorscheme = category + 3
h_span_colorscheme = w_span_colorscheme
w_span_button = 1
w_span_mdh = 1
w_span_photo = w_span_mdh + w_span_colorscheme
h_span_button = 11
h_span_mdh = h_span_colorscheme / 3
w_span_year = w_span_photo
h_span_year = 1
h_span_plotagg = h_span_colorscheme
w_span_graph = w_span_button * 4
h_span_graph = 1
h_span_photo = h_span_graph * 4
s_colorcell = 28
w_mdh_slider = w_window - (s_colorcell + 2) * w_span_colorscheme

row_photo = 0
col_photo = 0
row_empty = row_photo + h_span_photo
row_month = row_empty + 1
row_date = row_month + h_span_mdh
row_hour = row_date + h_span_mdh
row_year = row_hour + h_span_mdh
row_colorscheme = row_empty
row_plotagg = row_month
row_graph_0 = 0
row_button_0 = row_year

col_photo = 0
col_mdh = 0
col_colorscheme = col_mdh + w_span_mdh
col_year = 0
col_graph_0 = col_photo + w_span_photo
col_button_0 = col_graph_0
col_plotagg = col_graph_0

hour_start = 0
hour_end = 8759
interval = (hour_end - hour_start) / 10

def display(idx, time, imgName):
    hmap.plotImg(imgName)
    hmap.titleX(time, "TkDefaultFont", "L")

    # display curves
    plotGraph.plotAll(idx, lbound, ubound, lbound_total, ubound_total)

# control month, date, hour slider
def printimg3(event):
    evt_month = (month.get())
    evt_date = (date.get())
    evt_hour = (hour.get())
    idx = mdh2hour(evt_month, evt_date, evt_hour, numdays)
    allyear.set(idx)
    imgName = hour2imgName(idx, master.dimVar.get(), "recovery")
    time = mdh2str(evt_month, evt_date, evt_hour)
    display(idx, time, imgName)

def printimg(event):
    idx = allyear.get()
    imgName = hour2imgName(idx, master.dimVar.get(), "recovery")

    mdh = hour2mdh(idx)
    t_month = mdh[0]
    t_date = mdh[1]
    t_hour = mdh[2]
    time = mdh2str(t_month, t_date, t_hour)
    size = s_colorcell
    display(idx, time, imgName)

master = Tk()
w = str(w_graph * 2 + w_window + 10)
master.geometry(w+'x700+0+0')
master.title("Dynamic Heating-Cooling Map")
defaultbg = master.cget('bg')
bd_font = "TkDefault 8 bold"
nm_font = "TkDefault 8"
ot_font = "TkDefault 6"
font_color = "gray45"

# variables of option menu
master.typeVar = StringVar(master) # plot topic
master.typeVar.set("space heat")
master.numVar = StringVar(master)  # plot quantities
master.numVar.set("single")
master.timeVar = StringVar(master) # time interval and duration
master.timeVar.set("day")
master.dimVar = StringVar(master)  # 2D/3D toggle
master.dimVar.set("2D")
master.statVar = StringVar(master) # aggregation method
master.statVar.set("exact")

#reading in building information configuration
[bdCountDict, bdTypeDict, areaDict, initDict, bdSectorDict,bdFilenameDict] = ld.readLand()
bdTypelist = [key for key in bdCountDict]
bdinitlist = [initDict[key] for key in initDict]  # key is building type

def showTxt():
    msg = ld.generalMsg()
    heatmsg = Message(master,text = msg, font = bd_font, width =
                      category * s_colorcell, fg = font_color)
    heatmsg.grid(row = row_colorscheme, column = col_colorscheme,
                rowspan = h_span_colorscheme, columnspan =
                w_span_colorscheme)

def plotBuilding():
    dirname = "energyData/Community_"
    fileDict = {"space heat" : "spaceheat.csv", "cool" : "c_elec.csv",
                "recover" : "recov.csv", "electricity" : "elec.csv",
                "heat" : "heat.csv"}
    typeDict = {"space heat" : dfSpaceHeat, "cool" : dfCool,"heat" : dfHeat,
                "recover" : dfRecover, "electricity" : dfElec}
    (num, choice, period, step, title, stat) = plotMethod()
    filename = dirname + fileDict[choice]
    df = typeDict[choice]
    idx = allyear.get()
    numPeriod = 8760 // step
    if num == "single":
        f, axarr = plt.subplots(4, 4, sharex=True, sharey = True)
        for i in range(16):
            if stat == "exact":
                data = df.ix[idx: min(idx + step, 8760), i]
                windowTitle = "Single Building " + title
                g = data.plot(ax=axarr[i/4, i%4], title = bdTypelist[i])
                g.set_xlim(idx, min(idx + step, 8760) - 1)
            else:
                if stat == "peak":
                    data = pd.Series([(df.ix[y * step:(y + 1)*step, i]).max()
                                      for y in range(numPeriod)])
                elif stat == "average":
                    data = pd.Series([(df.ix[y * step:(y + 1)*step, i]).mean()
                                      for y in range(numPeriod)])
                elif stat == "total":
                    data = pd.Series([(df.ix[y * step:(y + 1)*step, i]).sum()
                                      for y in range(numPeriod)])
                windowTitle = 'Single Building {0} {1}'.format(stat.capitalize(), title)
                g = data.plot(ax=axarr[i/4, i%4], title = bdTypelist[i])
                g.set_xlim(0, numPeriod + 1)
    else:
        f, axarr = plt.subplots(2, 1, sharex = False, sharey = False)
        sr = pd.Series(np.genfromtxt(filename, delimiter = ','))

        g1 = sr[idx:(min(idx+step, 8760))].plot(ax = axarr[0], title = title)
        g1.set_xlim(idx, min(idx+step, 8760) - 1)

        if stat == "exact":
            sr2 = pd.Series([sr[idx%step + i*step] for i in range(numPeriod)])
            title = '{0} with step {1}'.format(title, period)
        else:
            if stat == "peak":
                sr2 = pd.Series([max(sr[i*step:(i + 1)*step])
                                for i in range(numPeriod)])
            if stat == "total":
                sr2 = pd.Series([sum(sr[i*step:(i + 1)*step])
                                for i in range(numPeriod)])
            if stat == "average":
                sr2 = pd.Series([ar.getAve(sr[i*step:(i + 1)*step])
                                for i in range(numPeriod)])
            title = '{0} {1} {2}'.format(stat.capitalize(), period+"ly", title)

        g2 = sr2.plot(ax = axarr[1], title = title)
        g2.set_xlim(0, numPeriod - 1)
        g2.axvline(idx//step, color = 'red', linestyle='--')
        g2.annotate('current', xy = (idx//step, sr[idx//step]))
        windowTitle = "Community " + title
    f.canvas.set_window_title(windowTitle)
    plt.show()

# show legend in a separate window
def showLegend():
    legendWd = Tk()
    # 2d legend object
    l_size = w_photo/4
    legend = Canvas(legendWd, width = l_size, height = l_size)
    legend.grid(row = row_colorscheme, column = col_colorscheme,
                rowspan = h_span_colorscheme, columnspan =
                w_span_colorscheme)
    x = cr.createColorScheme(legendWd, category, row_colorscheme,
                             col_colorscheme, s_colorcell,
                             "quantile", "energy recovery")
    (color_2d, coloridDict) = x
    colorGrid = cr.colorRamp_2d(category, [255, 255, 255],
                                [255, 0, 0], [0, 0, 255])

    size = s_colorcell
    for i in range(category):
        for j in range(category):
            f = color_2d[i][j]
            f.create_rectangle(0, 0, size, size, fill =
                            colorGrid[i][j], outline = defaultbg)

    # tick mark in 2d color ramp
    idx = allyear.get()
    for key in coloridDict:
        (h, c) = coloridDict[key][idx]
        g = color_2d[c][h]
        g.create_rectangle(0, 0, size, size, fill = colorGrid[c][h],
                        outline = defaultbg)
        g.create_text(size/2, size/2, fill = font_color,
                    font = bd_font, text = "x")
    legendWd.mainloop()

# functions to control buttons to jump forward and backward
def advance24h():
    allyear.set(allyear.get() + 24)
def advance1h():
    allyear.set(allyear.get() + 1)
def back24h():
    allyear.set(allyear.get() - 24)
def back1h():
    allyear.set(allyear.get() - 1)

# clear selected landuse for calculation
def clearSelect():
    global landSelection # modify the global copy
    landSelection = []
    hmap.g.delete("a")

# buttons to control advance and back
buttonList = [[{'text':'+24h', 'cmd':advance24h},
               {'text':'+1h', 'cmd':advance1h},
               {'text':'-24h', 'cmd':back24h},
               {'text':'-1h', 'cmd':back1h}],
              [{'text':'plot', 'cmd':plotBuilding},
               {'text':'legend', 'cmd':showLegend},
               {'text':'clear', 'cmd':clearSelect}]]

rowcount = 0
for row in buttonList:
    buttoncount = 0
    for button in row:
        button = Button(master, text = button['text'], command =
                        button['cmd'], width = w_button, font = bd_font,
                        fg = font_color)
        button.grid(row = row_button_0 + rowcount, column =
                    col_button_0 + buttoncount, rowspan =
                    h_span_button, columnspan = w_span_button)
        buttoncount += 1
    rowcount += 1

showTxt()

# create a canvas and display images on canvas
hmap = plotGraph.ImgPlot("Dynamic Heat Map", row_photo, col_photo,
                         h_span_photo, w_span_photo, w_window,
                         h_window, photo_lr, photo_lr, photo_tb,
                         photo_tb, master)
'''
def callback(event):
    with open ('landCord.txt', 'a') as wt:
        wt.write ('{0}, {1}, '.format(event.x, event.y))
        print event.x, event.y
'''
# reading a table with landuse and coordinates
def readLandShape():
    landDict = {}
    with open ('input/land.txt', 'r') as rd:
        rows = csv.reader(rd)
        for row in rows:
            key = str(row[1:])
            land = row[0]
            landDict[key] = land
    return landDict

(x, y) = ld.read2dicts()
allDict = dict(zip(x, y))
dfSpaceHeat = pd.DataFrame(allDict["Space Heating"])
dfHeat = pd.DataFrame(allDict["Heating"])
dfElec = pd.DataFrame(allDict["Electricity:Facility"])
dfCool = pd.DataFrame(allDict["Cooling:Electricity"])
dfRecover = pd.DataFrame(allDict["Heat Recover"])
landDict = readLandShape()
initialDict = dict([(initDict[key], key) for key in initDict])

landSelection = []

def plotMethod():
    titleDict = {"space heat" : "Space Heating Demand (kBtu)",
                 "cool" : "Space Cooling Demand (kBtu)",
                 "heat" : "Heating Demand (kBtu)",
                 "electricity" : "Electricity Demand (kBtu)",
                 "recover": "Energy Recovery Potential (kBtu)",
                 "single" : "", "group" : "Total ", "community":"Community "}
    typeDict = {"space heat" : dfSpaceHeat, "cool" : dfCool,"heat" : dfHeat,
                "recover" : dfRecover, "electricity" : dfElec}
    stepDict = {"day" : 24, "week" : (24*7), "month" : (24*30)}
    num = master.numVar.get()
    choice = master.typeVar.get()
    period = master.timeVar.get()
    stat = master.statVar.get()
    step = stepDict[period]
    title = titleDict[num] + titleDict[choice]
    return (num, choice, period, step, title, stat)

def landName(event):
    titleDict = {"space heat" : "Space Heating Demand (kBtu)",
                 "cool" : "Space Cooling Demand (kBtu)",
                 "heat" : "Heating Demand (kBtu)",
                 "electricity" : "Electricity Demand (kBtu)",
                 "recover": "Energy Recovery Potential (kBtu)",
                 "single" : "", "group" : "Total ", "community":"Community "}
    typeDict = {"space heat" : dfSpaceHeat, "cool" : dfCool,"heat" : dfHeat,
                "recover" : dfRecover, "electricity" : dfElec}
    pt = (event.x, event.y)
    for key in landDict:
        key2list = [int(x) for x in ast.literal_eval(key)]
        if geo.pointInPolygon(pt, key2list):
            landInit = landDict[key]
            bdtype = initialDict[landInit]
            hmap.g.create_polygon(tuple(key2list), fill = 'red', tag = 'a')
            landSelection.append(landInit)
            print 'Selection Set: {0}'.format(landSelection)
            print "landuse is {0}".format(landDict[key])
            idx = allyear.get()
            (num, choice, period, step, title, stat) = plotMethod()
            numPeriod = 8760 // step

            # plot for single building
            if num == "single":
                title = '{0} {1}'.format(bdtype, title)
                f, axarr = plt.subplots(2, 1, sharex=False, sharey = False)
                g1 = typeDict[choice][bdtype][idx:(min(idx+step, 8760))].plot(ax = axarr[0], title = title)
                g1.set_xlim(idx, min(idx+step, 8760) - 1)

                building = typeDict[choice][bdtype]
                if stat == "exact":
                    sr = pd.Series([building[idx%step + i*step]
                                    for i in range(numPeriod)])
                    title = '{0} with step {1}'.format(title, period)
                else:
                    if stat == "peak":
                        sr = pd.Series([max(building[i*step:(i + 1)*step])
                                        for i in range(numPeriod)])
                    if stat == "total":
                        sr = pd.Series([sum(building[i*step:(i + 1)*step])
                                        for i in range(numPeriod)])
                    if stat == "average":
                        sr = pd.Series([ar.getAve(building[i*step:(i + 1)*step])
                                        for i in range(numPeriod)])
                    title = '{0} {1} {2}'.format(stat.capitalize(), (period+"ly").capitalize(), title)
                g2 = sr.plot(ax = axarr[1],title = title)
                g2.set_xlim(0, numPeriod - 1)
                g2.axvline(idx//step, color = 'red', linestyle='--')
                g2.annotate('current', xy = (idx//step, sr[idx//step]))
            else:
                title = '{0} {1}'.format(landSelection, titleDict[choice])
                f, axarr = plt.subplots(2, 1, sharex=False, sharey = False)
                bdtypelst = [initialDict[x] for x in landSelection]
                selectDF = pd.DataFrame(typeDict[choice], columns = bdtypelst)
                print list(selectDF.columns.values)
                selectDF['agg'] = selectDF.sum(axis = 1)
                g1 = selectDF['agg'][idx:(min(idx+step, 8760))].plot(ax = axarr[0], title = title)
                g1.set_xlim(idx, min(idx+step, 8760) - 1)
                if stat == "exact":
                    sr = pd.Series([selectDF['agg'][idx%step + i*step]
                                    for i in range(numPeriod)])
                    title = '{0} with step {1}'.format(title, period)
                else:
                    if stat == "peak":
                        sr = pd.Series([max(selectDF['agg'][i*step:(i+1)*step])
                                       for i in range(numPeriod)])
                    elif stat == "average":
                        sr = pd.Series([ar.getAve(selectDF['agg'][i*step:(i+1)*step]) for i in range(numPeriod)])
                    elif stat == "total":
                        sr = pd.Series([sum(selectDF['agg'][i*step:(i+1)*step])
                                       for i in range(numPeriod)])

                    title = '{0} {1} {2}'.format(stat.capitalize(), (period+"ly").capitalize(), title)
                g2 = sr.plot(ax = axarr[1], title = title)
                g2.set_xlim(0, numPeriod - 1)
                g2.axvline(idx//step, color = 'red', linestyle='--')
                g2.annotate('current', xy = (idx//step, sr[idx//step]))
            plt.xlabel('time')
            title = titleDict[num] + titleDict[choice]
            plt.ylabel(titleDict[choice])
            plt.show()

            return
    print "invalid selection"

hmap.g.bind("<Button-1>", landName)

n_row = 4
n_col = 2
x = plotGraph.createAll(master, n_row, n_col, row_graph_0,
                        col_graph_0, h_span_graph, w_span_graph,
                        h_span_plotagg, w_span_graph)
(lbound, ubound, lbound_total, ubound_total) = x

empty = Canvas(width = w_mdh_slider, height = s_colorcell/2)
empty.grid(row = row_empty, column = col_mdh)

# month
month = Scale(master, from_= 1, length = w_mdh_slider, to =
              12,tickinterval=1, orient=HORIZONTAL, command =
              printimg3, label = "Month", width = w_scale, font =
              nm_font, activebackground = "red", fg = font_color)
month.set(1)
month.grid(row = row_month, column = col_mdh, rowspan = h_span_mdh,
           columnspan = w_span_mdh)

# date
date = Scale(master, from_= 1, to = 31, length = w_mdh_slider,
             tickinterval=7, orient=HORIZONTAL, command = printimg3,
             label = "Date", width = w_scale, font = nm_font,
             activebackground = "green", fg = font_color)
date.set(1)
date.grid(row = row_date, column = col_mdh, rowspan = h_span_mdh,
          columnspan = w_span_mdh)

# hour
hour = Scale(master, from_= 0, to = 23, length = w_mdh_slider,
             tickinterval=4, orient=HORIZONTAL, command = printimg3,
             label = "Hour", width = w_scale, font = nm_font,
             activebackground = "blue", fg = font_color)
hour.set(0)
hour.grid(row = row_hour, column = col_mdh, rowspan = h_span_mdh,
          columnspan = w_span_mdh)

# year slider
allyear = Scale(master, from_= hour_start, length = w_slider, to =
                hour_end, tickinterval=interval, orient=HORIZONTAL,
                command = printimg, label = "Year Round", width = 10,
                font = nm_font, fg = font_color)
allyear.set(0)
allyear.grid(row = row_year, column = col_year, rowspan = h_span_year,
             columnspan = w_span_year)

# cover the original label
monthTick = Canvas(master, width = w_slider, height = 15)
monthTick.grid(row = row_year, column = col_year, rowspan =
               h_span_year, columnspan = w_span_year, sticky = S)
monthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
             "Sep", "Oct", "Nov", "Dec"]
w_cursor = 15
for i in range(12):
    monthTick.create_line(w_cursor + 1 + w_slider/12*i, 1, w_cursor + 1 + w_slider/12*i, 8,
                          fill = font_color)
    monthTick.create_text(w_cursor + 26 + w_slider/12*i, 7, text = monthList[i],
                          font = nm_font, fill = font_color)

optbuttonList = [{'opt': ['single', 'group', 'community'],
                  'var':master.numVar},
                 {'opt': ['2D', '3D'], 'var' : master.dimVar},
                 {'opt': ['day', 'week', 'month'], 'var':master.timeVar}]
# option menu to choose the plot method
col_opt_0 = col_button_0 + len(buttonList[0])
count = 0
for item in optbuttonList:
    opt = OptionMenu(master, item['var'], *item['opt'])
    opt.grid(row = row_button_0, column = col_opt_0 + count, rowspan = h_span_button, columnspan = w_span_button, sticky = "ew")
    count += 1
optbuttonList = [{'opt': ['heat', 'cool', 'recover', 'space heat',
                          'electricity'], 'var':master.typeVar},
                 {'opt': ['exact', 'average', 'peak', 'total'],
                  'var':master.statVar}]
count = 0
for item in optbuttonList:
    opt = OptionMenu(master, item['var'], *item['opt'])
    opt.grid(row = row_button_0 + 1, column = col_opt_0 + count*2, rowspan = h_span_button, columnspan = w_span_button * 2, sticky = "ew")
    count += 1
mainloop()
