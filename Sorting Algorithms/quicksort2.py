import random

def sort(inlist):
    for i in range(len(inlist)):
        inlist[i] = float(inlist[i])
    outlist = sort_sublist(inlist)
    output = output_parser(outlist)
    return output

def sort_list(nlist):
    ranrange = random.randrange(0,len(nlist)-1)
    lista = []
    mnumber = nlist[ranrange]
    listb = [mnumber]
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

    outlist = []
    if len(lista) > 0:
        outlist.append(lista)
    outlist.append(listb)
    if len(listc) > 0:
        outlist.append(listc)

    return outlist

def sort_sublist(sublist):
    i = 0
    while i < len(sublist):
        if type(sublist[i]) == list:
            sublist[i] = sort_sublist(sublist[i])
        else:
            if len(sublist) > 1:
                sublist = sort_list(sublist)
                for j in range(len(sublist)):
                    sublist[j] = sort_sublist(sublist[j])
                i = len(sublist)
        i = i + 1
    return sublist

def output_parser(inputlist):
    outputlist = []
    for i in range(len(inputlist)):
        if type(inputlist[i]) == list:
            outputlist = outputlist + output_parser(inputlist[i])
        else:
            outputlist.append(inputlist[i])
    return outputlist
