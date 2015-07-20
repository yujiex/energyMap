from Tkinter import *
from util_time import *
import plotGraph
import colorRamp as cr

# ###############
# global setting of user interface
w_photo = plotGraph.w_photo
h_photo = plotGraph.h_photo
photo_tb = plotGraph.photo_tb
photo_lr = plotGraph.photo_lr
w_window = plotGraph.w_window
h_window = plotGraph.h_window
h_slider = plotGraph.h_slider

h_slider = 10
w_slider = w_window
w_button = 3
w_scale = 10

category = 7
w_span_colorscheme = category + 3
h_span_colorscheme = w_span_colorscheme
w_span_button = 1
w_span_mdh = 1
w_span_photo = w_span_mdh + w_span_colorscheme
h_span_button = 1
h_span_mdh = h_span_colorscheme / 3
w_span_year = w_span_photo
h_span_year = 1
h_span_plotagg = h_span_colorscheme
w_span_graph = w_span_button * 2
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

# functions to control buttons to jump forward and backward
def advance24h():
    allyear.set(allyear.get() + 24)

def advance1h():
    allyear.set(allyear.get() + 1)

def back24h():
    allyear.set(allyear.get() - 24)

def back1h():
    allyear.set(allyear.get() - 1)
    
def display(idx, time, imgName):
    size = s_colorcell
    for i in range(category):
        for j in range(category):
            f = color_2d[i][j]
            f.create_rectangle(0, 0, size, size, fill =
                               colorGrid[i][j], outline = defaultbg)

    # tick mark in 2d color ramp
    for key in coloridDict:
        (h, c) = coloridDict[key][idx]
        g = color_2d[c][h]
        g.create_rectangle(0, 0, size, size, fill = colorGrid[c][h],
                           outline = defaultbg)
        g.create_text(size/2, size/2, fill = font_color,
                      font = bd_font, text = "x")
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
    imgName = hour2imgName(idx)
    time = mdh2str(evt_month, evt_date, evt_hour)
    display(idx, time, imgName)

def printimg(event):
    idx = allyear.get()
    imgName = hour2imgName(idx)
    mdh = hour2mdh(idx)
    t_month = mdh[0]
    t_date = mdh[1]
    t_hour = mdh[2]
    time = mdh2str(t_month, t_date, t_hour)
    size = s_colorcell
    display(idx, time, imgName)

master = Tk()
master.title("Dynamic Heat Map")
defaultbg = master.cget('bg')
bd_font = "TkDefault 8 bold"
nm_font = "TkDefault 8"
ot_font = "TkDefault 6"
font_color = "gray45"

# buttons to control advance and back
buttonList = [{'text':'+24h', 'cmd':advance24h},
              {'text':'+1h', 'cmd':advance1h},
              {'text':'-24h', 'cmd':back24h},
              {'text':'-1h', 'cmd':back1h}]

buttoncount = 0
for button in buttonList:
    button = Button(master, text = button['text'], command =
                    button['cmd'], width = w_button, font = bd_font,
                    fg = font_color)
    button.grid(row = row_button_0, column = col_button_0 +
                buttoncount, rowspan = h_span_button, columnspan =
                w_span_button)
    buttoncount += 1

# create a canvas and display images on canvas
hmap = plotGraph.ImgPlot("Dynamic Heat Map", row_photo, col_photo,
                         h_span_photo, w_span_photo, w_window,
                         h_window, photo_lr, photo_lr, photo_tb,
                         photo_tb, master)

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
for i in range(12):
    monthTick.create_line(1 + w_slider/12*i, 1, 1 + w_slider/12*i, 8,
                          fill = font_color)
    monthTick.create_text(26 + w_slider/12*i, 7, text = monthList[i],
                          font = nm_font, fill = font_color)

# 2d legend object
l_size = w_photo/4
legend = Canvas(master, width = l_size, height = l_size)
legend.grid(row = row_colorscheme, column = col_colorscheme, rowspan =
            h_span_colorscheme, columnspan = w_span_colorscheme)
x = cr.createColorScheme(master, category, row_colorscheme,
                         col_colorscheme, s_colorcell, "quantile")
(color_2d, coloridDict) = x
colorGrid = cr.colorRamp_2d(category, [255, 255, 255],
                            [255, 0, 0], [0, 0, 255])

mainloop()
