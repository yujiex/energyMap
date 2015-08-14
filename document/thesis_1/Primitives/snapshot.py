'''
Created on Jun 5, 2015

@author: yujie
'''
from scripting import *
import time

# get a CityEngine instance
ce = CE()

def main():
    x = ce.getObjectsFrom(ce.scene, ce.withName("'LOT'"))  # < 1s
    for i in range(2):
        for item in x:
            ce.setAttribute(item, 'time', i) # 28 s
            views = ce.getObjectsFrom(ce.get3DViews())  # < 1s
        if i < 10:
            views[0].snapshot(ce.toFSPath('images')+("/img000"+str(i)+".png"))
        elif i < 100:
            views[0].snapshot(ce.toFSPath('images')+("/img00"+str(i)+".png"))
        elif i < 1000:
            views[0].snapshot(ce.toFSPath('images')+("/img0"+str(i)+".png"))
        else:
            views[0].snapshot(ce.toFSPath('images')+("/img"+str(i)+".png"))

if __name__ == '__main__':
    main()
    
    
