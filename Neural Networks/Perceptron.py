class Perceptron:
    def __init__(self,learning_rate,weights_or_weights_length):
        import random
        self.output = 0

        self.weights = []
        self.learning_rate = learning_rate
        if type(weights_or_weights_length) == list:
            self.weights_length = len(weights_or_weights_length) - 1
            for i in range(self.weights_length):
                self.weights.append(weights_or_weights_length[i])
        else:
            self.weights_length = weights_or_weights_length
            for i in range(self.weights_length + 1):
                self.weights.append((random.random() * 2) - 1)

    def sign(self,input_value):
        if input_value >= 0:
            return 1
        else:
            return -1

    def guess(self,inputs):
        input_sum = 0
        for i in range(len(inputs)):
            input_sum += inputs[i] * self.weights[i]
        input_sum += self.weights[self.weights_length]
        self.output = self.sign(input_sum)
        return self.output

    def train(self,inputs,target):
        guess_value = self.guess(inputs)
        error_value = target - guess_value
        for i in range(self.weights_length):
            self.weights[i] += error_value * inputs[i] * self.learning_rate
        self.weights[self.weights_length] += error_value * self.learning_rate
        if error_value == 0:
            return 1
        else:
            return 0
