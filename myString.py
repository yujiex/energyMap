# parse a substring between front:str and back:str
# requires: front:str and back:str in the string
# return the middle section between the front string and back string
def midStr(string, front, back):
    start = string.find(front) + len(front)
    if (start >= len(string)):
        return ""
    end = string.find(back, start)
    if not (end == -1):
        return string[start:end]
    else:
        return string[start:]

def testmidStr():
    assert(midStr("", "", "") == "")
    assert(midStr("", "abc", "") == "")
    assert(midStr("", "", "abc") == "")

    assert(midStr("aapsodifh", "", "abc") == "aapsodifh")
    assert(midStr("aapsodifh", "aa", "abc") == "psodifh")
    assert(midStr("aapsodifh", "a", "aps") == "")
    assert(midStr("aapsodifh", "so", "fh") == "di")
    print("All Test Passed!")

# #### #### #### #### #### ####
# not used in the interface
# #### #### #### #### #### ####
def parseHelper(string, sep, acc):
    if not sep in string:
        acc.append(string)
        return acc
    idx = string.index(sep)
    newString = string[(idx + 1):]
    seg = string[:idx]
    acc.append(seg)
    return parseHelper(newString, sep, acc)

# return a list of string
def parseStr(string, sep):
    return parseHelper(string, sep, [])

def testParseStr():
    assert(cmp(parseStr("", "-"), ['']) == 0)
    assert(cmp(parseStr("a", "-"), ["a"]) == 0)
    assert(cmp(parseStr("a-a", "-"), ["a", "a"]) == 0)
    assert(cmp(parseStr("a-b", "-"), ["a", "b"]) == 0)
    assert(cmp(parseStr("a-b-c-d", "-"), ["a", "b", "c", "d"]) == 0)

def main():
    testmidStr()
    test_list_cmp()
    testParseStr()

#main()
