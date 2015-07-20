#import numpy as np
import util_order as od
import bisect as bs

# helper function, return the prefix sum of the list
def prefixSum(mylist):
    preflist = []
    sumsofar = 0
    for item in mylist:
        sumsofar = sumsofar + item
        preflist.append(sumsofar)
    return preflist

def test_prefixSum():
    assert(prefixSum([]) == 0)
    assert(prefixSum([1]) == 1)
    assert(prefixSum([1, 2]) == [1, 3])
    assert(prefixSum([2, 1]) == [2, 3])

# scale mylist with ratio r
def scaleList(mylist, r):
    return [x * r for x in mylist]

def test_scaleList():
    assert(scaleList([], 3) == [])
    assert(scaleList([1], 3) == [3])
    assert(scaleList([1, 2, 3], 3) == [3, 6, 9])
    assert(scaleList([], 3.0) == [])
    assert(scaleList([1], 3.0) == [3.0])
    assert(scaleList([1, 2, 3], 3.0) == [3.0, 6.0, 9.0])
    assert(scaleList([], 3.0) == [])
    assert(scaleList([1.0], 3) == [3.0])
    assert(scaleList([1.0, 2.0, 3.0], 3) == [3.0, 6.0, 9.0])

# return the weight of each item in list
def weigh(lst):
    total = sum(lst)
    assert(len(lst) != 0)
    assert(total != 0)
    return [float(x) / total for x in lst]

def test_weigh():
    # do not test empty case
    assert(weigh([1]) == [1])
    assert(weigh([2]) == [1])
    assert(weigh([1, 1]) == [0.5, 0.5])
    assert(weigh([2, 3, 5]) == [0.2, 0.3, 0.5])

# produce weighted sum of a list list
def wt_sumLists(lists):
    result = []
    if len(lists) == 0:
        return result
    length = len(lists[0])
    if length == 0:
        return result
    for elt in lists:
        assert(len(elt) == length)
    if isinstance(lists[0][0], int) or isinstance(lists[0][0], float):
        for i in range(length):
            row = [x[i] for x in lists]
            result.append(np.average(row, weights = weigh(row)))
        return result
    elif isinstance(lists[0][0], list):
        for i in range(length):
            result.append(wt_sumLists([lst[i] for lst in lists]))
        return result
def test_wt_sumLists():
    assert(wt_sumLists([]) == [])
    assert(wt_sumLists([[], [], []]) == [])
    assert(np.allclose(wt_sumLists([[1], [2], [3]]), [7.0/3]))
    assert(np.allclose(wt_sumLists([[1, 1], [2, 2], [3, 3]]), [7.0/3,
                                                               7.0/3]))
    assert(wt_sumLists([[1], [1], [1]]) == [1])
    print(wt_sumLists([[1, 1], [2, 2]]))
    print(wt_sumLists([[1, 3], [2, 2], [3, 1]]))
    print(wt_sumLists([[[1], [3]], [[2], [2]], [[3], [1]]]))
    print(wt_sumLists([[[1, 1, 2], [2, 2, 1]], [[3, 3, 3], [1, 1,
                                                            1]]]))
    print(wt_sumLists([[], []]))
    print("All test passed!")

# require all list in lists with same length
def sumLists(lists):
    result = []
    if len(lists) == 0:
        return result
    length = len(lists[0])
    if length == 0:
        return result
    for elt in lists:
        assert(len(elt) == length)
    if isinstance(lists[0][0], int) or isinstance(lists[0][0], float):
        for i in range(length):
            acc = 0
            for lst in lists:
                acc += lst[i]
            result.append(acc)
        return result
    # if elements are list, return the list some of element
    elif isinstance(lists[0][0], list):
        for i in range(length):
            result.append(sumLists([lst[i] for lst in lists]))
        return result

def test_sumLists():
    assert(sumLists([]) == [])
    assert(sumLists([[], [], []]) == [])
    assert(sumLists([[1], [2], [3]]) == [6])
    assert(sumLists([[1, 1], [2, 2], [3, 3]]) == [6, 6])
    assert(sumLists([[1.0], [2.0], [3.0]]) == [6.0])
    print(sumLists([[1, 1], [2, 2]]))
    print(sumLists([[1, 3], [2, 2], [3, 1]]))
    print(sumLists([[[1], [3]], [[2], [2]], [[3], [1]]]))
    print(sumLists([[[1, 1, 2], [2, 2, 1]], [[3, 3, 3], [1, 1, 1]]]))
    print(sumLists([[], []]))

def scaleSum(datalists, countlist):
    assert(len(datalists) == len(countlist))
    scaled = [scaleList(x, y) for (x, y) in zip(datalists, countlist)]
    return sumLists(scaled)

def test_scaleSum():
    assert(scaleSum([], []) == [])
    assert(scaleSum([[], [], []], [1, 2, 3]) == [])
    assert(scaleSum([[1], [1], [1]], [1, 2, 3]) == [6])
    assert(scaleSum([[1.0], [1.0], [1.0]], [1, 2, 3]) == [6.0])
    assert(scaleSum([[1, 2], [1, 3], [1, 4]], [1, 2, 3]) == [6, 20])

# interpolation
def interp(mini, maxi, num_points):
    if num_points < 2:
        print("invalid number of category")
        return [] # invalid input
    interval = (float(maxi) - mini)/(num_points - 1)
    #print("interval = %f" % interval)
    if isinstance(mini, int): # type checking
        breakpoints = [int(round(mini + x * interval, 0))
                       for x in range(num_points - 1)] + [maxi]
    else:
        breakpoints = [mini + x * interval for x in
                       range(num_points - 1)] + [maxi]
    return breakpoints

def test_interp():
    assert(cmp(interp(1, 4, 1), []) == 0)
    assert(cmp(interp(4, 1, 1), []) == 0)
    assert(cmp(interp(1, 4, 2), [1, 4]) == 0)
    assert(cmp(interp(4, 1, 2), [4, 1]) == 0)
    assert(cmp(interp(1, 4, 3), [1, 3, 4]) == 0)
    assert(cmp(interp(4, 1, 3), [4, 3, 1]) == 0)
    assert(cmp(interp(1.0, 4.0, 3), [1.0, 2.5, 4.0]) == 0)
    assert(cmp(interp(1, 10, 4), [1, 4, 7, 10]) == 0)
    assert(cmp(interp(1.0, 10.0, 4), [1.0, 4.0, 7.0, 10.0]) == 0)
    assert(cmp(interp(1, 11, 4), [1, 4, 8, 11]) == 0)
    assert(np.allclose(interp(1.0, 11.0, 4), 
                       [1.0, 4.333333, 7.666667, 11.0], 
                       rtol = 0.0, atol = 0.01))
    print("All test passed!")

# breakpoints is in sorted order
# for all x in data, x is \in [min(breakpoints), max(breakpoints)]
def bucket(data, breakpoints):
    length = len(breakpoints)
    # prevent modifying global variable: breakpoints
    newbreakpoints = [x for x in breakpoints]
    assert(length != 0)
    newbreakpoints[length - 1] += 1
    newbreakpoints[0] -= 1
    return [od.lisearch(newbreakpoints, x, "floor") for x in data]
#   return [bs.bisect_left(newbreakpoints, x) for x in data]

# not the original function, need to repair @@
def test_bucket():
    assert(cmp(bucket([], [1, 2, 3]), []) == 0)
    print(bucket([1], [1, 2, 3]), [0])
    assert(cmp(bucket([1], [1, 2, 3]), [0]) == 0)
    assert(cmp(bucket([2, 3], [1, 2, 3]), [1, 1]) == 0)
    assert(cmp(bucket(list(range(1, 7)), [1, 4, 6]), [0, 0, 0, 1, 1,
                                                      1]) == 0)
    print("All test passed!")

#test_bucket()
