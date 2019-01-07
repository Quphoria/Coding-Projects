import MatrixMath
MX = MatrixMath.Matrix(2,3)
MX.printdata()
MX.randomise()
MX.mult(100)
MX.round()
MX.printdata()
MX.add(4)
MX.printdata()
MX.add_matrix(MX)
MX.printdata()
MX.transpose()
MX.printdata()
print(MX.get_val(1,2))
def double(input_value):
    return input_value * 2
MX.apply_funct(double)
MX.printdata()
MX2 = MatrixMath.Matrix(MX)
def subtract(input_value,values):
    return input_value - values[0]
MX.apply_funct(subtract,[4])
MX.printdata()
def average(input1,input2):
    return (input1+input2) / 2
MX.apply_funct_matrix(average,MX2)
MX.printdata()
def average_div(input1,input2,value):
    return ((input1+input2) / 2) / value[0]
MX.apply_funct_matrix(average_div,MX2,[3])
MX.printdata()
