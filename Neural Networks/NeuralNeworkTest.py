import NeuralNetwork, NeuralTraining, tkintercanvas, math
NN = NeuralNetwork.NeuralNetwork(2,2,1)
NN.learning_rate = 0.5

learning_correct_cycles = 50000
learning_max_cycles = 200000
learning_point_limit = 20000
testing_size = 20000

window_height = 700
window_width = 1300
point_size = 5
point_outlines = True

def point_funct(point_x,point_y):
    wx = point_x / window_width
    wy = point_y / window_height
    return 1 - abs(wx - wy)

    # return  0.001 * point_x * point_x - point_y

cbox = tkintercanvas.CanvasBox(window_width,window_height,point_size,"black","Learning...")
cbox.clear()

correct_cycles = 0
point_num = 0
while True:
    if point_num > learning_point_limit:
        point_num = 0
        cbox.clear()
    current_point = NeuralTraining.Point(point_funct,window_width,window_height)
    cbox.addPoint(current_point.x,current_point.y,point_num)
    cbox.pointColour(point_num,"white",point_outlines)

    input_values = [current_point.x/window_width*12,current_point.y/window_height*12]
    # print(input_values)
    output_values = NN.train(input_values,[current_point.target])
    # print(output_values)
    outcome = (output_values[0] * 2) - 1
    #outcome = (current_point.target * 2) - 1
    # print(outcome)
    outcome = max(min(outcome,1),-1)
    gval = int(255 * ((outcome + 1)/2))
    bval = int(255 * ((1 - outcome)/2))

    show_incorrect = True
    if abs(current_point.target - outcome) > 0.3 and show_incorrect:
        correct_cycles = 0
        # cbox.pointColour(point_num,"red",point_outlines)
        cbox.pointColourRGB(point_num,0,gval,bval,point_outlines,outline_R=255,outline_G=0,outline_B=0)
    else:
        correct_cycles += 1
        cbox.pointColourRGB(point_num,0,gval,bval,point_outlines,0,gval,bval)
        # if current_point.target > 0:
        #     cbox.pointColour(point_num,"green")
        # else:
        #     cbox.pointColour(point_num,"blue")
    cbox.update()
    point_num +=1
