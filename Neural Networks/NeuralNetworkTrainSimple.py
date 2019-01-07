import NeuralNetwork
NN = NeuralNetwork.NeuralNetwork(2,2,1)
inputs = [[0,0],[0,1],[1,0],[1,1]]
outputs = [[0],[1],[1],[0]]
while True:
    for i in range(len(inputs)):
        #print(inputs[i])
        #print(outputs[i])
        #print(NN.train(inputs[i],outputs[i]))
        #print(round(NN.train(inputs[i],outputs[i])[0]) == outputs[i][0])
        print(abs(NN.train(inputs[i],outputs[i])[0] - outputs[i][0]))
