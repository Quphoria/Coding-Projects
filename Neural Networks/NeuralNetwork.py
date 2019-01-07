class NeuralNetwork:
    def __init__(self,InputNodes, HiddenNodes, OutputNodes):
        import MatrixMath
        import math
        self.MatrixMath = MatrixMath
        self.math = math
        self.input_nodes_num = InputNodes
        self.hidden_nodes_num = HiddenNodes
        self.output_nodes_num = OutputNodes

        self.weights_matrix_ih = MatrixMath.Matrix(self.hidden_nodes_num,self.input_nodes_num)
        self.weights_matrix_ho = MatrixMath.Matrix(self.output_nodes_num,self.hidden_nodes_num)
        self.weights_matrix_ih.randomise()
        self.weights_matrix_ho.randomise()

        self.bias_matrix_h = MatrixMath.Matrix(self.hidden_nodes_num,1)
        self.bias_matrix_o = MatrixMath.Matrix(self.output_nodes_num,1)
        self.bias_matrix_h.randomise()
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

    def feedforward(self,input_array):
        #Generating Hidden Node Outputs
        inputs = self.MatrixMath.Matrix(input_array)
        hidden_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ih,inputs)
        hidden_matrix.add_matrix(self.bias_matrix_h)
        #Activation Function
        hidden_matrix.apply_funct(self.sigmoid)

        #Generating Output Node Outputs
        output_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ho,hidden_matrix)
        output_matrix.add_matrix(self.bias_matrix_o)
        #Activation Function
        output_matrix.apply_funct(self.sigmoid)
        return output_matrix.toArray()

    def train(self,input_array,answer_array):
        #Generating Hidden Node Outputs
        inputs = self.MatrixMath.Matrix(input_array)
        hidden_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ih,inputs)
        hidden_matrix.add_matrix(self.bias_matrix_h)
        #Activation Function
        hidden_matrix.apply_funct(self.sigmoid)

        #Generating Output Node Outputs
        output_matrix = self.MatrixMath.mult_matrix(self.weights_matrix_ho,hidden_matrix)
        output_matrix.add_matrix(self.bias_matrix_o)
        #Activation Function
        output_matrix.apply_funct(self.sigmoid)

        answer_matrix = self.MatrixMath.Matrix(answer_array)
        #answer_matrix.sub_matrix(output_matrix)

        #Calculate output errors
        output_errors = self.MatrixMath.Matrix(answer_array)
        output_errors.sub_matrix(output_matrix)

        weights_ho = self.MatrixMath.Matrix(self.weights_matrix_ho)
        weights_ho_trans = self.MatrixMath.Matrix(weights_ho)
        weights_ho_trans.transpose()
        hidden_errors = self.MatrixMath.mult_matrix(weights_ho_trans,output_errors)

        #Calculate Gradients
        gradients = self.MatrixMath.Matrix(output_matrix)
        gradients.apply_funct(self.dsigmoid)
        gradients.mult_matrix(output_errors)
        gradients.mult(self.learning_rate)

        hidden_gradients = self.MatrixMath.Matrix(hidden_matrix)
        hidden_gradients.apply_funct(self.dsigmoid)
        hidden_gradients.mult_matrix(hidden_errors)
        hidden_gradients.mult(self.learning_rate)

        #Calculate Deltas
        hidden_matrix_trans = self.MatrixMath.Matrix(hidden_matrix)
        hidden_matrix_trans.transpose()
        weights_ho_deltas = self.MatrixMath.mult_matrix(gradients,hidden_matrix_trans)

        inputs_matrix_trans = self.MatrixMath.Matrix(inputs)
        inputs_matrix_trans.transpose()
        weights_ih_deltas = self.MatrixMath.mult_matrix(hidden_gradients,inputs_matrix_trans)

        #Adjust weights
        self.weights_matrix_ho.add_matrix(weights_ho_deltas)
        self.bias_matrix_o.add_matrix(gradients)
        self.weights_matrix_ih.add_matrix(weights_ih_deltas)
        self.bias_matrix_h.add_matrix(hidden_gradients)

        return output_matrix.toArray()
