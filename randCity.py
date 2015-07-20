from Tkinter import *
import random as rd

import util_loadData as ld
import util_array as ar
from util_time import *
import colorRamp as cl

master = Tk()
master.title("random city")
defaultbg = master.cget('bg')

# global settings
dim = 10    # city dimension
size = 40   # bd size
h_time = 20
density = 0.3
bdTypelist = ["Green", "FullServiceRestaurant", "Hospital",
              "LargeHotel", "LargeOffice", "MediumOffice",
              "MidriseApartment", "OutPatient", "PrimarySchool",
              "QuickServiceRestaurant", "SecondarySchool",
              "SmallHotel", "SmallOffice", "Stand-aloneRetail",
              "StripMall", "SuperMarket", "Warehouse"]

bdinitlist = ["", "FR", "HO", "LH", "LO", "MO", "MA", "OP", "PS", "QR",
              "SS", "SH", "SO", "SR", "SM", "SU", "WH"]
category = 7

bd_font = "TkDefault 8 bold"
ot_font = "TkDefault 6"
font_color = "gray45"

# loaddata
heatDict = ld.profile2Dict("energyData/meterData/", "Heating:Gas")
coolDict = ld.profile2Dict("energyData/meterData/", "Cooling:Elec")

# functions for buttons
def advance24h():
    allyear.set(allyear.get() + 24)

def advance1h():
    allyear.set(allyear.get() + 1)

def back24h():
    allyear.set(allyear.get() - 24)

def back1h():
    allyear.set(allyear.get() - 1)

# create a starting board of random city
def createBoard(n_row, n_col, size):
    f_matrix = []
    l_matrix = []
    bd_cnt = [0] * 17
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
                landuse = rd.randint(1, 16)
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

(f_2d, l_2d, bd_count) = createBoard(dim, dim, size)
countDict = dict(zip(bdTypelist, bd_count))
del countDict["Green"]

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
              {'text':'-1h', 'cmd':back1h, 'col' : 6}]

for button in buttonList:
    f_button = Button(master, text = button['text'], command =
                      button['cmd'], width = w_button, font = bd_font,
                      fg = font_color)
    f_button.grid(row = row_button, column = button['col'], columnspan
                  = 2)

mainloop()
