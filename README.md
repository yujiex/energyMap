# energyMap

Project Dixcrition: Dynamic Energy Map User Interface Design

## Author(s):

Yujie Xu

## Purpose:
The main interface (manySlider.py) enables user to view dynamic
changes of heating and cooling demand of a conceptual urban
environment setting.

## General Functions:

The heating and cooling demand profile is generated from DOE benchmark
building (post 1980) and is color coded with a two dimensional color
ramp. The energy demand information is demonstrated with data plot on
the right of the interface, the 3D urban space model on the top left
and the "tick marks" on the lower left. The navigation between
different time of year (one of the 8760 hours) is controlled by a
series of sliders: one all-year-round slider on the bottom left and
three stepped sliders that control jumping with specific steps of
month, day and hour.  

## Interface Layout: 

![Interface Layout of Dynamic Energy Demand Map]
(https://github.com/yujiex/energyMap/blob/master/interfaceSnapshot/interface0720.png)

# randCity

Testbed for data classification and representation

## Author(s):

Yujie Xu

## Purpose:

The primary purpose of this interface is to test the effectiveness of
some color scheme and classification method on some randomly generated
conceptual city layout. Originally it is a side-product of the data
classification and visualization, but it might open up a new path in
the future.  

## General Function: 

Each time the interface is launched, a random axa (default to be
10x10) city with specified urban density (default to be 30%) will be
initialized, where a is the number of building lot on each side of the
city, the default setting is 10x10. The energy demand profile is also
retrieved from simulation of DOE benchmark models (post 1980). One can
navigate through different time of year with a slider and four buttons
on the bottom and visualize the color code for each time step.

For the current setting, the heating demand, and cooling demand data
is classified with "quantile" method into 7 categories. The color of
the building is then decided with the categories the heating and
cooling demand belongs to. For example, if a building consumes 100
kbtu heating energy and 90 kbtu of cooling energy at time t. The
classification breakpoint for heating is [0, 200, 300] and the
breakpoint for cooling is [0, 50, 100], then the heating category for
this building at time t is 0 and the cooling category for the building
at time t is 1, so the color for the building is the color depicted at
the 1st row 0th column in the 2d color ramp.

## Interface Layout: 

![Interface Layout of Dynamic Energy Demand Map]
(https://github.com/yujiex/energyMap/blob/master/interfaceSnapshot/randCity.png)
