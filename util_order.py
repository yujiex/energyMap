# requires data not empty
from bisect import *
def findMinMax(data):
    length = len(data)
    assert(length > 0)
    maxi = data[0]
    mini = maxi
    for x in data:
        if (cmp(x, mini) < 0):
            mini = x
        elif (cmp(x, maxi) > 0):
            maxi = x
    return (mini, maxi)

def test_findMinMax():
    assert(findMinMax([0, 1, 2]) == (0, 2))
    assert(findMinMax([2, 1, 0]) == (0, 2))
    assert(findMinMax([0.0, 1.0, 2.0]) == (0.0, 2.0))
    assert(findMinMax([2.0, 1.0, 0.0]) == (0.0, 2.0))
    assert(findMinMax(['a', 'b', 'c']) == ('a', 'c'))

def findInterval(item, lst):
    length = len(lst)
    for i in range(length):
        if item <= lst[i]:
            return i
    return None

# linear search items in a sorted array
# floor: return first i: list[i] <= key, None otherwise
# ceil: return first i: list[i] >= key, None otherwise
# exact: return first i: list[i] == key, None otherwise
def lisearch(items, key, method):
    length = len(items)
    if length == 0:
        return None
    elif length == 1:
        if (method == "floor" and cmp(key, items[0]) >= 0):
            return 0
        elif (method == "ceil" and cmp(key, items[0]) <= 0):
            return 0
        elif (method == "exact" and cmp(key, items[0]) == 0):
            return 0
        else:
            return None
    else:
        if method == "floor":
            for i in range(length - 1):
                if cmp(key, items[i]) >= 0 and cmp(key, items[i+1])< 0:
                    return i
            if cmp(key, items[length - 1]) == 0:
                return length - 1
        if method == "ceil":
            for i in range(length - 1):
                if cmp(key, items[i]) <= 0:
                    return i
            if cmp(key, items[length - 1]) <= 0:
                return length - 1
        if method == "exact":
            for i in range(length):
                if cmp(key, items[i]) == 0:
                    return i
        return None

def test_lisearch_exact():
    assert (lisearch([], 0.0, "exact") == None)
    assert (lisearch([1.0], 0.0, "exact") == None)
    assert (lisearch([1.0], 1.0, "exact") == 0)
    # even length
    arr = [x * 1.0 for x in range(5)]
    assert (lisearch(arr, 0.0, "exact") == 0)
    assert (lisearch(arr, 1.0, "exact") == 1)
    assert (lisearch(arr, 1.5, "exact") == None)
    assert (lisearch(arr, 2.0, "exact") == 2)
    assert (lisearch(arr, 2.5, "exact") == None)
    assert (lisearch(arr, 3.0, "exact") == 3)
    assert (lisearch(arr, 4.0, "exact") == 4)
    assert (lisearch(arr, 5.0, "exact") == None)
    # odd length
    arr = [x * 1.0 for x in range(4)]
    assert (lisearch(arr, 0.0, "exact") == 0)
    assert (lisearch(arr, 1.0, "exact") == 1)
    assert (lisearch(arr, 1.5, "exact") == None)
    assert (lisearch(arr, 2.0, "exact") == 2)
    assert (lisearch(arr, 3.0, "exact") == 3)

def test_lisearch_floor():
    # test of floor
    assert (lisearch([], 0.0, "floor") == None)
    assert (lisearch([1.0], 0.0, "floor") == None)
    assert (lisearch([1.0], 1.5, "floor") == 0)
    assert (lisearch([1.0], 1.0, "floor") == 0)
    # even length
    arr = [x * 1.0 for x in range(5)]
    assert (lisearch(arr, 0.0, "floor") == 0)
    assert (lisearch(arr, 1.0, "floor") == 1)
    assert (lisearch(arr, 1.5, "floor") == 1)
    assert (lisearch(arr, 2.0, "floor") == 2)
    assert (lisearch(arr, 2.5, "floor") == 2)
    assert (lisearch(arr, 3.0, "floor") == 3)
    assert (lisearch(arr, 4.0, "floor") == 4)
    assert (lisearch(arr, 5.0, "floor") == None)
    # odd length
    arr = [x * 1.0 for x in range(4)]
    assert (lisearch(arr, 0.0, "floor") == 0)
    assert (lisearch(arr, 1.0, "floor") == 1)
    assert (lisearch(arr, 1.5, "floor") == 1)
    assert (lisearch(arr, 2.0, "floor") == 2)
    assert (lisearch(arr, 2.5, "floor") == 2)
    assert (lisearch(arr, 3.0, "floor") == 3)
    print("All Test Passed!")

def test_lisearch_ceil():
    # test of floor
    assert (lisearch([], 0.0, "ceil") == None)
    assert(findInterval(0.0, []) == lisearch([], 0.0, "ceil"))
    assert (lisearch([1.0], 0.0, "ceil") == 0)
    assert (lisearch([1.0], 0.0, "ceil") == findInterval(0.0, [1.0]))
    assert (lisearch([1.0], 1.5, "ceil") == None)
    assert (lisearch([1.0], 1.5, "ceil") == findInterval(1.5, [1.0]))
    assert (lisearch([1.0], 1.0, "ceil") == 0)
    assert (lisearch([1.0], 1.0, "ceil") == findInterval(1.0, [1.0]))
    # even length
    arr = [x * 1.0 for x in range(5)]
    assert (lisearch(arr, 0.0, "ceil") == 0)
    assert (lisearch(arr, 1.0, "ceil") == 1)
    assert (lisearch(arr, 1.5, "ceil") == 2)
    assert (lisearch(arr, 2.0, "ceil") == 2)
    assert (lisearch(arr, 2.5, "ceil") == 3)
    assert (lisearch(arr, 3.0, "ceil") == 3)
    assert (lisearch(arr, 4.0, "ceil") == 4)
    assert (lisearch(arr, 5.0, "ceil") == None)
    # odd length
    arr = [x * 1.0 for x in range(4)]
    assert (lisearch(arr, 0.0, "ceil") == 0)
    assert (lisearch(arr, 1.0, "ceil") == 1)
    assert (lisearch(arr, 1.5, "ceil") == 2)
    assert (lisearch(arr, 2.0, "ceil") == 2)
    assert (lisearch(arr, 2.5, "ceil") == 3)
    assert (lisearch(arr, 3.0, "ceil") == 3)
    print("All Test Passed!")

#test_lisearch_ceil()
