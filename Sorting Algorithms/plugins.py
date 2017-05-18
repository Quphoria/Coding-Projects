def reverse(tlist):
    rolist = []
    for i in range(len(tlist)):
        rolist.append(tlist.pop())
    return rolist

def remove_dp(tlist):
    rolist = []
    for i in range(len(tlist)):
        data = tlist[i]
        if data % 1 == 0:
            data = int(data)
        rolist.append(data)
    return rolist
