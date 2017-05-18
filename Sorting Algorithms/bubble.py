def sort(sortlist):
    outlist = []
    x = 0
    lsize = len(sortlist)
    while x < lsize:
        smlst = sortlist[0]
        for i in range(len(sortlist)):
            if float(sortlist[i]) < float(smlst):
                smlst = sortlist[i]
        sortlist.remove(smlst)
        outlist.append(float(smlst))
        x += 1
    return outlist
