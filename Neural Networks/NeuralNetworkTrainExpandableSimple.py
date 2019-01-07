import NeuralNetworkExpandable
NN = NeuralNetworkExpandable.NeuralNetwork(2,[2],1)
inputs = [[0,0],[0,1],[1,0],[1,1]]
outputs = [[0],[1],[1],[0]]
while True:
    for i in range(len(inputs)):
        #print("-----")
        #print(inputs[i])
        #print(outputs[i])
        guess = NN.train(inputs[i],outputs[i])
        print(guess[0] - outputs[i][0])
