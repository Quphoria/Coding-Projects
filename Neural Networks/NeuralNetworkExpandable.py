class NeuralNetwork:
    def __init__(self,InputNodes, HiddenNodesList, OutputNodes):
        import MatrixMath
        import math
        self.MatrixMath = MatrixMath
        self.math = math
        self.input_nodes_num = InputNodes
        self.hidden_nodes_num = HiddenNodesList
        self.hidden_nodes_num_len = len(HiddenNodesList)
        self.output_nodes_num = OutputNodes

        self.weights_matrix_ih = MatrixMath.Matrix(self.hidden_nodes_num[0],self.input_nodes_num)
        self.weights_matrix_ho = MatrixMath.Matrix(self.output_nodes_num,self.hidden_nodes_num[len(HiddenNodesList)-1])
        self.weights_matrix_ih.randomise()
        self.weights_matrix_ho.randomise()

        self.weights_matrixes_hh = []
        for i in range(self.hidden_nodes_num_len-1):
            self.weights_matrixes_hh.append(MatrixMath.Matrix(self.hidden_nodes_num[i+1],self.hidden_nodes_num[i]))
            self.weights_matrixes_hh[i].randomise()

        self.bias_matrixes_h = []
        for i in range(self.hidden_nodes_num_len):
            self.bias_matrixes_h.append(MatrixMath.Matrix(self.hidden_nodes_num[i],1))
            self.bias_matrixes_h[i].randomise()

        self.bias_matrix_o = MatrixMath.Matrix(self.output_nodes_num,1)
        self.bias_matrix_o.randomise()

        self.learning_rate = 0.1

    def sigmoid(self,x):
        # return x
        # print(x)
        # return self.math.erfc(x)
        return 1 / (1 + self.math.exp(-x))

    def dsigmoid(self,y):
        #return self.sigmoid(y) * (1 - self.sigmoid(y))
        return y * (1 - y)

    def feedforwardhidden(self,input_matrix,hidden_matrix_id):
        #Generating Hidden Node Outputs
        inputs = self.MatrixMath.Matrix(input_matrix)
        hidden_matrix = self.MatrixMath.mult_matrix(self.weights_matrixes_hh[hidden_matrix_id-1],inputs)
        hidden_matrix.add_matrix(self.bias_matrixes_h[hidden_matrix_id])
        #Activation Function
        hidden_matrix.apply_funct(self.sigmoid)

        return hidden_matrix

    def feedforward(self,input_array):
        #Generating Hidden Node Outputs
        inputs = self.MatrixMath.Matrix(input_array)
        hidden_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ih,inputs)
        hidden_matrix.add_matrix(self.bias_matrixes_h[0])
        #Activation Function
        hidden_matrix.apply_funct(self.sigmoid)

        for i in range(self.hidden_nodes_num_len - 1):
            hidden_matrix = self.feedforwardhidden(hidden_matrix,i + 1)

        #Generating Output Node Outputs
        output_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ho,hidden_matrix)
        output_matrix.add_matrix(self.bias_matrix_o)
        #Activation Function
        output_matrix.apply_funct(self.sigmoid)
        return output_matrix.toArray()

    def backpropogatehidden(self,following_errors,next_weights):
        weights_from = self.MatrixMath.Matrix(next_weights)
        weights_from.transpose()

        hidden_errors = self.MatrixMath.Matrix(weights_from)
        hidden_errors.mult_matrix(following_errors)
        return hidden_errors

    def adjusthiddenweights(self,hidden_layer_id):
        pass

    def train(self,input_array,answer_array):
        # Make Guess
        #Generating Hidden Node Outputs
        inputs = self.MatrixMath.Matrix(input_array)
        hidden_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ih,inputs)
        hidden_matrix.add_matrix(self.bias_matrixes_h[0])
        #Activation Function
        hidden_matrix.apply_funct(self.sigmoid)

        for i in range(self.hidden_nodes_num_len - 1):
            hidden_matrix = self.feedforwardhidden(hidden_matrix,i + 1)

        #Generating Output Node Outputs
        output_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ho,hidden_matrix)
        output_matrix.add_matrix(self.bias_matrix_o)
        #Activation Function
        output_matrix.apply_funct(self.sigmoid)

        #Calculate output errors
        output_errors = self.MatrixMath.Matrix(answer_array)
        output_errors.sub_matrix(output_matrix)
        #output_errors.printdata()

        #Calculate errors for hidden layers
        hidden_errors_layers = []
        hidden_errors = self.backpropogatehidden(output_errors,self.weights_matrix_ho)
        hidden_errors_layers.append(hidden_errors)

        for i in reversed(range(self.hidden_nodes_num_len - 1)):
            hidden_errors = self.backpropogatehidden(hidden_errors,self.weights_matrixes_hh[i])
            hidden_errors_layers.append(hidden_errors)
        hidden_errors_layers.reverse()

        #Calculate Gradients

        #Calculate Deltas

        #Adjust output weights


        #Adjust hidden layer weights

        return output_matrix.toArray()
