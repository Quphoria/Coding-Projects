import math

def funct_if(test,var_true,var_false):
    if (test):
        return var_true
    else:
        return var_false

def scale(var_old_min, var_old_max, var_new_min, var_new_max, var_value):
    OldSRange = (var_old_max - var_old_min)
    NewSRange = (var_new_max - var_new_min)
    return (((var_value - var_old_min) * NewSRange) / OldSRange) + var_new_min

def is_even(value_to_test):
    return value_to_test % 2 == 0

def draw_funct(dfunction, dxmin, dxmax, dymin, dymax, resolution):
    dx = scale(0,canvas_width,dxmin,dxmax,x)
    cdy = eval(dfunction)

    dx = scale(0,canvas_width,dxmin,dxmax,x-resolution)
    pdy = eval(dfunction)

    dx = scale(0,canvas_width,dxmin,dxmax,x+resolution)
    ndy = eval(dfunction)

    cdsy = canvas_height - scale(dymin,dymax,0,canvas_height,cdy)
    pdsy = canvas_height - scale(dymin,dymax,0,canvas_height,pdy)
    ndsy = canvas_height - scale(dymin,dymax,0,canvas_height,ndy)

    dyval = scale(0,canvas_height,dymin,dymax,y)
    py = scale(dymin,dymax,0,canvas_height,dyval-resolution)
    ny = scale(dymin,dymax,0,canvas_height,dyval+resolution)


    #if y - cdsy > py - pdsy and y - cdsy < ny - ndsy:
    #if (cdsy - y < pdsy - y and cdsy - y > ndsy - y) or (cdsy - y > pdsy - y and cdsy - y < ndsy - y):
    if (0 < pdsy - y and 0 > ndsy - y) or (0 > pdsy - y and 0 < ndsy - y) or round(cdsy - y) == 0:
    # print("dx: " + str(dx) + " , dy: " + str(dy))
    # if y - dsy < resolution + 1 and y - dsy > 0-(resolution + 1): #round(dsy) == y:
        return 255
    else:
        return 0
