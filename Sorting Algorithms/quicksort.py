import random

def sort(inlist):
    for i in range(len(inlist)):
        inlist[i] = float(inlist[i])
    listlen = len(inlist)
    inlist = [inlist]
    while len(inlist) < listlen:
        print(str(len(inlist)) + "/" + str(listlen))
        slist= []
        for i in range(len(inlist)):
            try:
                if len(inlist[i]) > 1:
                    slist = slist + sort_list(inlist[i])
                else:
                    slist = slist + inlist[i]
            except:
                slist = slist + [[inlist[i]]]
        inlist = slist
    outlist = []
    for i in range(len(inlist)):
        if type(inlist[i]) == list:
            outlist.append(inlist[i][0])
        else:
            outlist.append(inlist[i])
    return outlist

def sort_list(nlist):
    ranrange = random.randrange(0,len(nlist)-1)
    lista = []
    mnumber = nlist[ranrange]
    listb = [[mnumber]]
    listc = []
    for i in range(len(nlist)):
        if i != ranrange:
            cnumber = nlist[i]
            if cnumber < mnumber:
                lista.append(cnumber)
            elif cnumber == mnumber:
                listb.append([cnumber])
            else:
                listc.append(cnumber)


    if len(lista) > 0:
        outlist = [lista]
    else:
        outlist = []
    outlist = outlist + listb
    if len(listc) > 0:
        outlist = outlist + [listc]

    return outlist
