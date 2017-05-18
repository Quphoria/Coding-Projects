def check(inlist,lorder):
    result = True
    x = 1
    if lorder == 0:
        while result and x < len(inlist):
            if float(inlist[x-1]) <= float(inlist[x]):
                result = True
            else:
                result = False
            x = x + 1
    elif lorder == 1:
        while result and x < len(inlist):
            if float(inlist[x-1]) >= float(inlist[x]):
                result = True
            else:
                result = False
            x = x + 1
    else:
        result = False
    return result
