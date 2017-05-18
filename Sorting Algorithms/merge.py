from plugins import reverse

def l_merge(lista,listb):
    listm = []
    lista = reverse(lista)
    listb = reverse(listb)
    loada = True
    loadb = True
    while (len(lista) > 0 or not loada) and (len(listb) > 0 or not loadb):
        if loada:
            tmpa = lista.pop()
            loada = False
        if loadb:
            tmpb = listb.pop()
            loadb = False
        if tmpa <= tmpb:
            listm.append(tmpa)
            loada = True
        else:
            listm.append(tmpb)
            loadb = True

    if not loada:
        listm.append(tmpa)
    if not loadb:
        listm.append(tmpb)

    if len(lista) > 0:
        listm = listm + reverse(lista)
    elif len(listb) > 0:
        listm = listm + reverse(listb)
    return listm


def sort(inlist):
    olist = []
    tmplist = []
    divlevels = []
    divalevels = []
    divrlevels = []
    clevel = 2
    nlen = divmod(len(inlist), clevel)
    while nlen[0] > 0:
        divlevels.append(clevel)
        divalevels.append(nlen[0])
        divrlevels.append(nlen[1])
        clevel = clevel * 2
        nlen = divmod(len(inlist), clevel)

    for i in range(len(inlist)):
        tmplist.append([float(inlist[i])])


    for j in range(len(divlevels)):
        clevel = divlevels[j]
        k = 0
        tmplistn = []
        while k < len(tmplist):
            tmpa = tmplist[k]
            if k + 1 < len(tmplist):
                tmpb = tmplist[k + 1]
                tmpc = l_merge(tmpa,tmpb)
            else:
                tmpc = tmpa
            tmplistn.append(tmpc)
            k = k + 2
        tmplist = tmplistn
    if len(tmplist) > 1:
        olist = l_merge(tmplist[0],tmplist[1])
    else:
        olist = tmplist[0]
    return olist
