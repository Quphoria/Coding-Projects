class Matrix:
    def __init__(self,y_size_or_matrix,x_size=None,inital_value=None):
        import pandas
        import random
        self.pandas = pandas
        self.random = random
        if x_size != None and inital_value != None:
            self.y_size = y_size_or_matrix
            self.x_size = x_size
            self.data = []
            for i in range(self.y_size):
                self.data.append([])
                for j in range(self.x_size):
                    self.data[i].append(inital_value)
        elif x_size != None:
            self.y_size = y_size_or_matrix
            self.x_size = x_size
            self.data = []
            for i in range(self.y_size):
                self.data.append([])
                for j in range(self.x_size):
                    self.data[i].append(0)
        else:
            if type(y_size_or_matrix) == list:
                self.x_size = 1
                self.y_size = len(y_size_or_matrix)
                self.data = []
                for i in range(len(y_size_or_matrix)):
                    self.data.append([y_size_or_matrix[i]])
            else:
                self.x_size = y_size_or_matrix.x_size
                self.y_size = y_size_or_matrix.y_size
                self.data = []
                for i in range(self.y_size):
                    self.data.append([])
                    for j in range(self.x_size):
                        self.data[i].append(y_size_or_matrix.data[i][j])

    def toArray(self):
        output_array = []
        for i in range(self.y_size):
            for j in range(self.x_size):
                output_array.append(self.data[i][j])
        return output_array

    def clone(self,matrixvar):
        self.x_size = (matrixvar.x_size)
        self.y_size = (matrixvar.y_size)
        self.data = []
        for i in range(y_size):
            self.data.append([])
            for j in range(x_size):
                self.data.append(matrixvar.data[i][j])

    def get_val(self,y_pos,x_pos):
        return self.data[x_pos][y_pos]

    def randomise(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] = (self.random.random()*2) - 1

    def set_val(self,var):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] = var

    def printdata(self):
        print()
        print(self.pandas.DataFrame(self.data))
        print()

    def add(self,var):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] += var

    def sub(self,var):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] -= var

    def mult(self,var):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] *= var

    def div(self,var):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] /= var

    def div_safe(self,var):
        if var == 0:
            set_value(0)
        else:
            for i in range(self.y_size):
                for j in range(self.x_size):
                    self.data[i][j] += var

    def round(self):
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] = round(self.data[i][j])

    def map_values(self,old_min,old_max,new_min,new_max):
        new_scale = (new_max - new_min) / (old_max - old_min)
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.data[i][j] = new_min + ((self.data[i][j] - old_min) * new_scale)

    def add_matrix(self,matrixvar):
        output = True
        tempdata = self.data
        if self.y_size == matrixvar.y_size and self.x_size == matrixvar.x_size:
            for i in range(self.y_size):
                if output:
                        for j in range(self.x_size):
                            if output:
                                try:
                                    tempdata[i][j] += matrixvar.data[i][j]
                                except:
                                    output = False
        else:
            output = False
        if output:
            self.data = tempdata
        return output

    def sub_matrix(self,matrixvar):
        output = True
        tempdata = self.data
        if self.y_size == matrixvar.y_size and self.x_size == matrixvar.x_size:
            for i in range(self.y_size):
                if output:
                        for j in range(self.x_size):
                            if output:
                                try:
                                    tempdata[i][j] -= matrixvar.data[i][j]
                                except:
                                    output = False
        else:
            output = False
        if output:
            self.data = tempdata
        return output

    def mult_matrix(self,matrixvar):
        output = True
        tempdata = self.data
        if self.y_size == matrixvar.y_size and self.x_size == matrixvar.x_size:
            for i in range(self.y_size):
                if output:
                        for j in range(self.x_size):
                            if output:
                                try:
                                    tempdata[i][j] *= matrixvar.data[i][j]
                                except:
                                    output = False
        else:
            output = False
        if output:
            self.data = tempdata
        return output


    def transpose(self):
        tempdata = []
        y_size = self.x_size
        x_size = self.y_size
        for i in range(y_size):
            tempdata.append([])
            for j in range(x_size):
                tempdata[i].append(self.data[j][i])
        self.data = tempdata
        self.y_size = y_size
        self.x_size = x_size

    def apply_funct(self,funct,arguments=None):
        output = True
        tempdata = self.data
        if arguments != None:
            for i in range(self.y_size):
                if output:
                        for j in range(self.x_size):
                            if output:
                                try:
                                    tempdata[i][j] = funct(tempdata[i][j],arguments)
                                except:
                                    output = False
        else:
            for i in range(self.y_size):
                if output:
                        for j in range(self.x_size):
                            if output:
                                try:
                                    tempdata[i][j] = funct(tempdata[i][j])
                                except:
                                    output = False
        if output:
            self.data = tempdata
        return output

    def apply_funct_matrix(self,funct,matrixvar,arguments=None):
        output = True
        tempdata = self.data
        if self.y_size == matrixvar.y_size and self.x_size == matrixvar.x_size:
            if arguments != None:
                for i in range(self.y_size):
                    if output:
                            for j in range(self.x_size):
                                if output:
                                    try:
                                        tempdata[i][j] = funct(tempdata[i][j],matrixvar.data[i][j],arguments)
                                    except:
                                        output = False
            else:
                for i in range(self.y_size):
                    if output:
                            for j in range(self.x_size):
                                if output:
                                    try:
                                        tempdata[i][j] = funct(tempdata[i][j],matrixvar.data[i][j])
                                    except:
                                        output = False
        else:
            output = False
        if output:
            self.data = tempdata
        return output

def mult_matrix(matrix1,matrix2):
    if matrix1.x_size == matrix2.y_size:
        output = Matrix(matrix1.y_size,matrix2.x_size,0)
        for i in range(output.y_size):
            for j in range(output.x_size):
                value_sum = 0
                for k in range(matrix1.x_size):
                    value_sum += matrix1.data[i][k] * matrix2.data[k][j]
                output.data[i][j] = value_sum
        return output
    else:
        return None
