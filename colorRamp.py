from Tkinter import *
import pandas as pd
import util_loadData as ld

import myString as ms
import util_array as ar
# run with python -O *.py to disable debug mode

'''
# for testing
master = Tk()
master.title("colorRamp")
'''
# mix colors in lists: for all x in lists, x is a color ramp in rgb
# format, for all y in x, y = [r, g, b]
def mixColor(lists):
    if len(lists) == 0:
        return []
    length = len(lists[0])
    mix_rgb = ar.sumLists(lists)

    # average the rgb value
    ave_rgb = [ar.scaleList(x, 1.0/len(lists)) for x in mix_rgb]
    ave_rgb = [[int(round(y, 0)) for y in x] for x in ave_rgb]

    # modulo
    round_rgb = [[y % 256 for y in x] for x in mix_rgb]

    # weighted average
    wt_mix_rgb = ar.wt_sumLists(lists)
    wt_mix_rgb = [[int(round(y, 0)) for y in x] for x in wt_mix_rgb]
    # change "wt_mix_rgb" to other value:
    # ave_rgb, round_rgb to see their effect
    mix_hex = [rgb2hex(x[0], x[1], x[2]) for x in wt_mix_rgb]
    return mix_hex

# r, g, b:int, return hx:string
def rgb2hex(r, g, b):
    hx = ("#" + (hex(r)[2:]).zfill(2) + (hex(g)[2:]).zfill(2) +
          (hex(b)[2:]).zfill(2)).upper()
    return hx

def test_rgb2hex():
    colorTable = pd.read_csv("color/color.csv")
    for i in range(554):
        R = colorTable.iloc[i, 2]
        G = colorTable.iloc[i, 3]
        B = colorTable.iloc[i, 4]
        H = colorTable.iloc[i, 1]
        assert(rgb2hex(int(R), int(G), int(B)) == H)

# rgb_start, rgb_end: int list
def colorInterp(num_points, rgb_start, rgb_end):
    rgb_list = [ar.interp(s, e, num_points)
                for (s, e) in zip(rgb_start, rgb_end)]
    return [[rgb_list[0][i], rgb_list[1][i], rgb_list[2][i]] for i in
            range(num_points)]

def test_colorInterp():
    print(colorInterp(5, [0, 0, 0], [255, 255, 255]))

# return 2d array of color in hex
def colorRamp_2d(num_points, rgb_origin, rgb_x, rgb_y):
    rgb_xy = [(a + b) for (a, b) in zip(rgb_x, rgb_y)]
    col_0 = colorInterp(num_points, rgb_origin, rgb_y)
    col_n = colorInterp(num_points, rgb_x, rgb_xy)
    arr = [colorInterp(num_points, col_0[i], col_n[i]) for i in
           range(num_points)]
    arr = [[rgb2hex(x[0], x[1], x[2]) for x in y] for y in arr]
    return arr

def colorRamp_1d(num_points, rgb_0, rgb_t):
    arr = colorInterp(num_points, rgb_0, rgb_t)
    arr = [rgb2hex(x[0], x[1], x[2]) for x in arr]
    return arr

def test_colorRamp_1d():
    num_points = 7
    rgb_0 = [255, 255, 255]
    rgb_t = [255, 0, 0]
    x = colorRamp_1d(num_points, rgb_0, rgb_t)
    for j in range(num_points):
        f = Canvas(master, width = 50, height = 50)
        f.create_rectangle(0, 0, 50, 50, fill = x[j])
        f.grid(row = 0, column = j)

def test_colorRamp_2d():
    num_points = 7
    ori_color = [255, 255, 255]
    x_color = [255, 0, 0]
    y_color = [0, 255, 0]
    color_2d = colorRamp_2d(num_points, ori_color, x_color, y_color)
    for i in range(num_points):
        for j in range(num_points):
            f = Canvas(master, width = 50, height = 50)
            f.create_rectangle(0, 0, 50, 50, fill = color_2d[i][j])
            f.grid(row = i, column = j)

def createColorScheme(master, cate, row_off, col_off, gridsize,
                      method, topic):
    bd_font = "TkDefault 7 bold"
    ot_font = "TkDefault 6"
    font_color = "gray45"
    defaultbg = master.cget('bg')
    (heat_breakpt,cool_breakpt,coloridDict) = data2breakpoints(cate,
                                                               method, topic)
    if topic == "energy recovery":
        colorGrid = colorRamp_2d(cate, [255, 255, 255],
                                 [255, 0, 0], [0, 0, 255])
    else:
        colorGrid = colorRamp_2d(cate, [255, 255, 255],
                                 [255, 0, 0], [0, 255, 0])

    heat_label = Canvas(master, width = gridsize, height = gridsize/2)
    heat_label.grid(row = row_off, column = col_off + cate + 2)
    heat_label.create_text(gridsize/2, gridsize/4, text = "High", font
                           = bd_font, fill = font_color)

    w_ht_dmd = gridsize * cate
    h_ht_dmd = gridsize/2
    ht_dmd_label = Canvas(master, width = w_ht_dmd, height = h_ht_dmd)
    ht_dmd_label.grid(row = row_off, column = col_off + 2, columnspan
                      = cate)
    ht_dmd_label.create_text(w_ht_dmd/2, h_ht_dmd/2,
                             text = "HEAT DEMAND", font = bd_font,
                             fill = font_color)

    zero_label = Canvas(master, width = gridsize, height = gridsize/2)
    zero_label.grid(row = row_off, column = col_off)
    zero_label.create_text(gridsize/2, gridsize/4, text = "Zero", font
                           = bd_font, fill = font_color)

    h_cl_dmd = gridsize * cate
    w_cl_dmd = gridsize
    cl_dmd_label = Canvas(master, width = w_cl_dmd, height = h_cl_dmd)
    cl_dmd_label.grid(row = row_off + 2, column = col_off, rowspan =
                      cate)
    if topic == "energy recovery":
        cl_dmd_label.create_text(w_cl_dmd/2, h_cl_dmd/2, text =
                                 "\n".join("COOL DEMAND"), font = bd_font,
                                 fill = font_color)
    else:
        cl_dmd_label.create_text(w_cl_dmd/2, h_cl_dmd/2, text =
                                 "\n".join("ELEC DEMAND"), font = bd_font,
                                 fill = font_color)

    row_cl_label = row_off + 2 + cate
    cool_label = Canvas(master, width = gridsize, height = gridsize)
    cool_label.grid(row = row_cl_label, column = col_off)
    cool_label.create_text(gridsize/2, gridsize/2, text = "High", font
                           = bd_font, fill = font_color)

    row_break = row_off + 1
    col_break = col_off + 1
    for i in range(cate + 1):
        f = Canvas(master, width = gridsize, height = gridsize/2)
        f.grid(row = row_break, column = i + col_break + 1)
        f.create_text(2, gridsize/2, anchor = SW, font = ot_font, fill
                      = font_color, text =
                      str(int(round(heat_breakpt[i], 0))))
        g = Canvas(master, width = gridsize, height = gridsize)
        g.grid(row = i + row_break + 1, column = col_break)
        g.create_text(gridsize, 0, anchor = NE, font = ot_font, fill =
                      font_color, text =
                      str(int(round(cool_breakpt[i], 0))))

    f_color = []
    for i in range(cate):
        row_color = []
        for j in range(cate):
            f = Canvas(master, width = gridsize, height = gridsize)
            f.grid(row = i + row_break + 1, column = j + col_break + 1)
            f.create_rectangle(0, 0, gridsize, gridsize, fill =
                               colorGrid[i][j], outline = defaultbg)
            row_color.append(f)
        f_color.append(row_color)
    return (f_color, coloridDict)

# return an array of colors with
# code: "rgb" or "hex"
def colorRamp(num_points, colorRamp, code):
    colorTable = pd.read_csv("color/color.csv")
    idx_df = colorTable.set_index(["NAME"])
    [startColor, endColor] = ms.parseStr(colorRamp, "-")
    rgb_start = [int(idx_df.loc[startColor, "R"]),
                 int(idx_df.loc[startColor, "G"]),
                 int(idx_df.loc[startColor, "B"])]
    rgb_end = [int(idx_df.loc[endColor, "R"]),
               int(idx_df.loc[endColor, "G"]),
               int(idx_df.loc[endColor, "B"])]
    # [R_list, G_list, B_list]
    rgb_list = [ar.interp(s, e, num_points)
                for (s, e) in zip(rgb_start, rgb_end)]
    if code == "hex":
        hex_list = []
        for i in range(num_points):
            r = rgb_list[0][i]
            g = rgb_list[1][i]
            b = rgb_list[2][i]
            string = rgb2hex(r, g, b)
            hex_list.append(string)
        return hex_list
    elif code == "rgb":
        color_list = []
        for i in range(num_points):
            r = int(rgb_list[0][i])
            g = int(rgb_list[1][i])
            b = int(rgb_list[2][i])
            color_list.append([r, g, b])
        return color_list

def test_colorRamp():
    num_cate =10
    rampType_r = "white*-red 1 (red*)"
    palette = colorRamp(num_cate, rampType_r, "hex")
    for i in range(num_cate):
        f = Canvas(master, width = 50, height = 50)
        f.create_rectangle(0, 0, 50, 50, fill = palette[i])
        f.grid(row = 0, column = i)
    rampType_b = "blue*-white*"
    palette = colorRamp(num_cate, rampType_b, "hex")
    for i in range(num_cate):
        f = Canvas(master, width = 50, height = 50)
        f.create_rectangle(0, 0, 50, 50, fill = palette[i])
        f.grid(row = 1, column = i)
    c1 = colorRamp(num_cate, rampType_r, "rgb")
    c2 = colorRamp(num_cate, rampType_b, "rgb")
    palette_mix = mixColor([c1, c2])
    for i in range(num_cate):
        f = Canvas(master, width = 50, height = 50)
        f.create_rectangle(0, 0, 50, 50, fill = palette_mix[i])
        f.grid(row = 2, column = i)

def data2breakpoints(cate, method, topic):
    (x, y) = ld.read2dicts()
    allDict = dict(zip(x, y))
    if (topic == "energy recovery"):
        heatDict = allDict["Space Heating"]
        coolDict = allDict["Cooling:Electricity"]
    else:
        heatDict = allDict["Heating"]
        coolDict = allDict["Electricity:Facility"]
    countDict = ld.bdCountDict
    totalheat = ld.total_count(countDict, heatDict)
    totalheat = [x for x in totalheat if x != 0.0]
    totalcool = ld.total_count(countDict, coolDict)
    totalcool = [x for x in totalcool if x != 0.0]
    breakpt_heat = ld.breakpt(totalheat, cate, method, False)
    breakpt_cool = ld.breakpt(totalcool, cate, method, False)
    coloridDict = {}
    for key in heatDict:
        if countDict[key] > 0:
            coloridDict[key] = zip(ar.bucket(heatDict[key],
                                             breakpt_heat),
                                   ar.bucket(coolDict[key],
                                             breakpt_cool))
    return(breakpt_heat, breakpt_cool, coloridDict)

import util_loadData as ld
import csv

def writeColor(topic, method, category, dirname, istocga, length=None):
    (breakpt_heat, breakpt_cool, x) = data2breakpoints(category,
                                                       "quantile", topic)
    (x, y) = ld.read2dicts()
    allDict = dict(zip(x, y))
    if (topic == "energy recovery"):
        heatDict = allDict["Space Heating"]
        coolDict = allDict["Cooling:Electricity"]
        colorGrid = colorRamp_2d(category, [255, 255, 255],
                                 [255, 0, 0], [0, 0, 255])
        colorHeat = colorRamp_1d(category, [255, 255, 255], [255, 0, 0])
        colorCool = colorRamp_1d(category, [255, 255, 255], [0, 0, 255])
    else:
        heatDict = allDict["Heating"]
        coolDict = allDict["Electricity:Facility"]
        colorGrid = colorRamp_2d(category, [255, 255, 255],
                                 [255, 0, 0], [0, 255, 0])
        colorHeat = colorRamp_1d(category, [255, 255, 255], [255, 0, 0])
        colorCool = colorRamp_1d(category, [255, 255, 255], [0, 255, 0])
    countDict = ld.bdCountDict

#   length = 20
    if length is None:
        length = 8760
    colorDict = {}
    colorHeatDict = {}
    colorCoolDict = {}
    for key in heatDict:
        # breakpoint calculated with "quantile" method cannot be used
        # to classify other data
        if countDict[key] != 0:
            heat_class = ar.bucket(heatDict[key], breakpt_heat)
            cool_class = ar.bucket(coolDict[key], breakpt_cool)
            color_profile = []
            color_pro_heat = []
            color_pro_cool = []
            for i in range(length):
                heatId = heat_class[i]
                coolId = cool_class[i]
                color_profile.append(colorGrid[coolId][heatId])
                color_pro_heat.append(colorHeat[heatId])
                color_pro_cool.append(colorHeat[coolId])
            colorHeatDict[key] = color_pro_heat
            colorCoolDict[key] = color_pro_cool
    if not istocga:
        for key in colorDict:
            filename = dirname + key + topic + "Color.txt"
            with open (filename, "w") as wt:
                mywriter = csv.writer(wt, delimiter=";")
                mywriter.writerow(colorDict[key])
            print("write to file: " + filename)
    else: # write to a file directly pasted to cga
        half = length/2
        filename = dirname + topic + "Color.txt"
        with open (filename, "w") as wt:
            mywriter = csv.writer(wt, delimiter=";")
            for key in colorDict:
                # in classification, max value might not be encountered
                mix = colorDict[key][:half]
                mix[0] = key + "_01 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)

                mix = colorDict[key][half:]
                mix[0] = key + "_02 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)
                print("write to row: " + key)

        filename = dirname + topic + "-heat-Color.txt"
        with open (filename, "w") as wt:
            mywriter = csv.writer(wt, delimiter=";")
            for key in colorHeatDict:
                # in classification, max value might not be encountered
                mix = colorHeatDict[key][:half]
                mix[0] = key + "_01 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)

                mix = colorHeatDict[key][half:]
                mix[0] = key + "_02 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)
                print("write to row: " + key)

        filename = dirname + topic + "-cool-Color.txt"
        with open (filename, "w") as wt:
            mywriter = csv.writer(wt, delimiter=";")
            for key in colorCoolDict:
                # in classification, max value might not be encountered
                mix = colorHeatDict[key][:half]
                mix[0] = key + "_01 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)

                mix = colorCoolDict[key][half:]
                mix[0] = key + "_02 = '" + mix[0]
                mix[-1] = mix[-1] + "'"
                mywriter.writerow(mix)
                print("write to row: " + key)

def testReal_2d():
    category = 7
    heatDict = ld.profile2Dict("energyData/meterData/", "Heating:Gas")
    coolDict = ld.profile2Dict("energyData/meterData/", "Cooling:Elec")
    length = 8760
    color_2d = colorRamp_2d(category,
                            [255, 255, 255], [255, 0, 0], [0, 0, 255])
    key = "Hospital"
    testlength = 50
    arr_heat = ld.classify(heatDict[key][:testlength], category,
                           "quantile")
    arr_cool = ld.classify(coolDict[key][:testlength], category,
                           "quantile")

    # get seperate color
    color_heat = colorRamp(category, "white*-red 1 (red*)", "rgb")
    color_cool = colorRamp(category, "white*-blue*", "rgb")
    arr_cl_heat = [color_heat[x] for x in arr_heat]
    arr_cl_cool = [color_cool[x] for x in arr_cool]
    arr_cl_heat = [rgb2hex(x[0], x[1], x[2]) for x in arr_cl_heat]
    arr_cl_cool = [rgb2hex(x[0], x[1], x[2]) for x in arr_cl_cool]

    gridwidth = 20
    for i in range(testlength):
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth, fill =
                           arr_cl_heat[i])
        f.grid(row = 0, column = i)
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth, fill =
                           arr_cl_cool[i])
        f.grid(row = 1, column = i)
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth,
                           fill = color_2d[arr_cool[i]][arr_heat[i]])
        f.grid(row = 2, column = i)

def testReal():
    category = 7
    heatDict = ld.profile2Dict("energyData/meterData/", "Heating:Gas")
    coolDict = ld.profile2Dict("energyData/meterData/", "Cooling:Elec")
    color_heat = colorRamp(category, "white*-red 1 (red*)", "rgb")
    color_cool = colorRamp(category, "white*-blue*", "rgb")
    length = 8760

#   for key in heatDict:
    key = "Hospital"
    testlength = 50

    heat_bp = ld.breakpt(heatDict[key][:testlength], category,
                         "quantile")
    cool_bp = ld.breakpt(coolDict[key][:testlength], category,
                         "quantile")
    arr_heat = ld.classify(heatDict[key][:testlength], heat_bp)
    arr_cool = ld.classify(coolDict[key][:testlength], cool_bp)
    arr_cl_heat = [color_heat[x] for x in arr_heat]
    arr_cl_cool = [color_cool[x] for x in arr_cool]
    mix = mixColor([arr_cl_heat, arr_cl_cool])
    arr_cl_heat = [rgb2hex(x[0], x[1], x[2]) for x in arr_cl_heat]
    arr_cl_cool = [rgb2hex(x[0], x[1], x[2]) for x in arr_cl_cool]

    gridwidth = 20
    for i in range(testlength):
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth, fill =
                           arr_cl_heat[i])
        f.grid(row = 0, column = i)
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth, fill =
                           arr_cl_cool[i])
        f.grid(row = 1, column = i)
        f = Canvas(master, width = gridwidth, height = gridwidth)
        f.create_rectangle(0, 0, gridwidth, gridwidth, fill = mix[i])
        f.grid(row = 2, column = i)

'''
# for testing
test_colorRamp()
test_rgb2hex()
test_colorInterp()
testReal_2d()
testReal()
test_colorRamp_2d()
test_colorRamp_1d()
createColorScheme(master, 7, 0, 0, 30, "quantile", "CHP")
mainloop()
'''
#writeColor("energy recovery", "quantile", 7, "color/convert/", True)
#writeColor("CHP", "quantile", 7, "color/convert/", True)
