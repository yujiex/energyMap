from Tkinter import *
import util_loadData as ld

# reading energy Data from files processed by energy data
from numpy import genfromtxt
def readEnergyData(filename):
    return genfromtxt(filename, delimiter = ',')

# style control
nm_font = "TkDefault 8"

# margin settings for graph plot
left = 40
right = 11
top = 20
bottom = 25

w_photo = 600
h_photo = 280
photo_tb = 25 # photo top bottom margin
photo_lr = 5  # photo left right margin
w_window = photo_lr * 2 + w_photo
h_window = photo_tb * 2 + h_photo

graph_height = h_window / 4 - 1
graph_width = w_photo / 2

# height of the aggregated heat demand
h_aggregateGraph = graph_height * 3.3
num_slider = 4
h_slider = h_aggregateGraph / 4 * 1.0

'''
# used for testing
master = Tk()
master.title("plotGraph")
'''

# get data slice of 24 hour
def getSlice(data, start, length):
    dataLength = len(data)
    if (start + length <= dataLength):
        return data[start:start + length]
    elif (dataLength < length):
        return data
    else:
        return data[dataLength - length:dataLength]

# normalize y axis of plot
def scaleRatio(maxi, mini, x):
    return ((x - mini) / (maxi - mini))

# create a canvas on (row_idx, col_idx)
# with row span and column span of row_sp, col_sp
# canvas dimension is c_width x c_height
# margins are left, right, top, bottom
class CanvasWtMargin(object):
    def __init__(self, title, row_idx, col_idx, row_sp, col_sp, c_width,
                 c_height, left, right, top, bottom, master):
        self.w_canvas = c_width
        self.h_canvas = c_height
        self.margin_l = left
        self.margin_r = right
        self.margin_t = top
        self.margin_b = bottom
        self.w_graph = self.w_canvas - self.margin_l - self.margin_r
        self.h_graph = self.h_canvas - self.margin_t - self.margin_b
        self.graph_t = self.margin_t
        self.graph_m = self.margin_t + self.h_graph / 2
        self.graph_b = self.margin_t + self.h_graph
        self.graph_r = self.w_canvas - self.margin_r
        self.graph_l = self.margin_l
        self.graph_c = self.margin_l + self.w_graph / 2
        self.xTitle_b = self.h_canvas - self.margin_b / 2
        self.xTitle_t = self.margin_t / 2

        self.title = title

        self.g = Canvas(master, width = c_width, height = c_height)
        self.g.grid(row = row_idx, column = col_idx,
                    rowspan = row_sp, columnspan = col_sp)

    # make top and bottom titles for the graph
    def titleX(self, title_b, ft, align):
        x_label = self.graph_c
        aln_b = N
        aln_t = CENTER
        if align == "L":
            x_label = self.graph_l + 7
            aln_b = W
            aln_t = NW
        self.g.create_text(x_label, self.xTitle_b,
                           text = title_b, anchor = aln_b, font=ft)
        self.g.create_text(x_label, self.xTitle_t, anchor = aln_t,
                           text = self.title, font=ft)

    def __repr__(self):
        d = self.__dict__
        results = [type(self).__name__ + "("]  # or: self.__class__.__name__
        for key in sorted(d.keys()):
            if (len(results) > 1): results.append(", ")
            results.append(key + "=" + repr(d[key]))
        results.append(")")
        return "".join(results)

# create a margined canvas that holds the main image
class ImgPlot(CanvasWtMargin):
    def plotImg(self, imgName):
        self.g.create_rectangle(0, 0, self.w_canvas, self.h_canvas,
                                fill = "white", outline = "white")
        photo = PhotoImage(file = imgName)
        img = Label(image = photo)
        img.image = photo
        self.g.create_image(self.graph_c, self.graph_m + 10, image =
                            photo)

# create a margined canvas that plots data
class DataPlot(CanvasWtMargin):
    def __init__(self, title, row_idx, col_idx, row_sp, col_sp,
                 c_width, c_height, datapath, left, right, top,
                 bottom, master):
        CanvasWtMargin.__init__(self, title, row_idx, col_idx, row_sp,
                                col_sp, c_width, c_height, left,
                                right, top, bottom, master)
        self.data = readEnergyData(datapath)

    #draw label of x axis
    def drawLabelX(self, start, step, length, interval):
        for i in range(start, length, step):
            x = self.margin_l + i*interval
            self.g.create_text(x, self.graph_b, text = str(i),
                               anchor = N, font = "TkDefault 6")
    def drawLabelY(self, value, y):
        datagraph_l = self.margin_l - 5
        self.g.create_text(datagraph_l, y, text = str(value),
                           font="TkDefault 6", anchor = E)

    # plotting the curve of data
    def drawCurve(self, data, maxi, mini, interval):
        num_data = len(data)
        for i in range(num_data - 1):
            x0 = self.margin_l + i*interval
            x1 = self.margin_l + (i + 1)*interval
            y0 = self.graph_b
            y1 = y0
            # prevent division by 0
            if (maxi - mini > 0):
                y0 = (self.margin_t + 
                      self.h_graph*(1 - scaleRatio(maxi,mini,data[i])))
                y1 = (self.margin_t +
                      self.h_graph*(1 - scaleRatio(maxi, mini,
                                                   data[i + 1])))
            self.g.create_line(x0, y0, x1, y1)

    # plot a single graph
    def plotSingle(self, idx, length, lower, upper):
        data = getSlice(self.data, idx, length)
        # (0, 0)indicate dynamic range adjust to the current data slice
        if (lower == 0.0 and upper == 0.0):
            mini = min(data)
            maxi = max(data)
        else:
            mini = lower
            maxi = upper
        ave = (maxi + mini) / 2
        interval = 1.0 * self.w_graph / (length - 1)

        self.g.create_rectangle(0, 0, self.w_canvas, self.h_canvas,
                                  fill = "white", outline = "white")
        self.drawLabelY(int(mini), self.graph_b)
        self.drawLabelY(int(maxi), self.graph_t)
        self.drawLabelY(int(ave), self.graph_m)

        self.g.create_rectangle(self.margin_l, self.margin_t,
                                  self.graph_r, self.graph_b,
                                  fill = 'white', outline = "#d8d8d8")

        self.drawCurve(data, maxi, mini, interval)
        self.drawLabelX(0, 4, length, interval)
        self.titleX("Time (Hour)", nm_font, "C")

graphList = []

sectorList = ["Hotel", "Office", "Residencial", "Commercial", "Total"]
titleList = [[i + " Heat Demand (Gas/kbtu)", 
              i + " Cool Demand (Electricity/kbtu)"] 
             for i in sectorList]
pathList = [["energyData/" + i + "_gas.csv", "energyData/" + i +
             "_elec.csv"] for i in sectorList]

# create all data plot object
def createAll(master, num_row_gr, num_col_gr, row_gr_0, col_gr_0,
              h_span_gr, w_span_gr, h_span_agg, w_span_agg):
    for i in range(num_row_gr):
        for j in range(num_col_gr):
            f = DataPlot(titleList[i][j], i * h_span_gr + row_gr_0, 
                         j * w_span_gr + col_gr_0, h_span_gr, 
                         w_span_gr, graph_width, graph_height, 
                         pathList[i][j], left, right, top, bottom,
                         master)
            graphList.append(f)
    maxi = max([max(f.data) for f in graphList])
    mini = min([min(f.data) for f in graphList])

    # total heat demand plot span many row
    row_agg = row_gr_0 + num_row_gr * h_span_gr
    for j in range(num_col_gr):
        f = DataPlot(titleList[4][j], row_agg, 
                     col_gr_0 + j * w_span_gr, h_span_agg, w_span_agg, 
                     graph_width, h_aggregateGraph, pathList[4][j], 
                     left, right, top, bottom, master)
        graphList.append(f)
    maxi_total = max([max(f.data) for f in graphList])
    mini_total = min([min(f.data) for f in graphList])
    return (mini, maxi, mini_total, maxi_total)

def plotAll(idx, lower, upper, lower_total, upper_total):
    length = len(graphList)
    for i in range(length - 2):
        graphList[i].plotSingle(idx, 25, lower, upper)
    graphList[length - 2].plotSingle(idx, 25, lower_total, upper_total)
    graphList[length - 1].plotSingle(idx, 25, lower_total, upper_total)

def test():
    createAll(0, 0, master)
    plotAll(0, 0.0, 0.0)

#mainloop()
