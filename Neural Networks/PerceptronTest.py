import Perceptron, PerceptronTraining, tkintercanvas, math

learning_rate_coarse = 0.0001
learning_rate_medium = 0.0000001
learning_rate_fine = 0.000000000001
learning_rate = learning_rate_coarse

medium_rate_threshold = 0.7
fine_rate_threshold = 0.55

Pct = Perceptron.Perceptron(learning_rate,2)

learning_correct_cycles = 50000
learning_max_cycles = 200000
learning_point_limit = 5000
testing_size = 20000

window_height = 600
window_width = 1200
point_size = 5
point_outlines = False

def point_funct(point_x,point_y):
    return  0.001 * point_x * point_x - point_y

#Learning time!
cbox = tkintercanvas.CanvasBox(window_width,window_height,point_size,"black","Learning...")
cbox.clear()

learning_cycles = learning_max_cycles
correct_cycles = 0
point_num = 0
while correct_cycles < learning_correct_cycles and learning_cycles > 0:
    if point_num > learning_point_limit:
        point_num = 0
        cbox.clear()
    current_point = PerceptronTraining.Point(point_funct,window_width,window_height)
    cbox.addPoint(current_point.x,current_point.y,point_num)
    cbox.pointColour(point_num,"white",point_outlines)
    outcome = Pct.train([current_point.x,current_point.y],current_point.target)
    print(Pct.weights)
    if outcome == 0:
        correct_cycles = 0
        cbox.pointColourRGB(point_num,255,0,0,point_outlines)
    else:
        correct_cycles += 1
        if current_point.target > 0:
            cbox.pointColourRGB(point_num,0,255,0,point_outlines)
        else:
            cbox.pointColourRGB(point_num,0,0,255,point_outlines)
    cbox.update()
    point_num += 1
    learning_cycles -= 1
    if learning_max_cycles * fine_rate_threshold > learning_cycles:
        if learning_rate != learning_rate_fine:
            learning_rate = learning_rate_fine
            Pct.learning_rate = learning_rate
    elif learning_max_cycles * medium_rate_threshold > learning_cycles:
        if learning_rate != learning_rate_medium:
            learning_rate = learning_rate_medium
            Pct.learning_rate = learning_rate
if learning_cycles <= 0:
    print("Max cycles reached.")
cbox.window.destroy()
#Testing time!
cbox = tkintercanvas.CanvasBox(window_width,window_height,point_size,"black","Testing...")
cbox.clear()

points = []
for i in range(testing_size):
    points.append(PerceptronTraining.Point(point_funct,window_width,window_height))
    cbox.addPoint(points[i].x,points[i].y,i)
    cbox.pointColour(i,"white",point_outlines)
cbox.update()

correct_guesses = 0
for i in range(testing_size):
    if Pct.guess([points[i].x,points[i].y]) == points[i].target:
        correct_guesses += 1
        if points[i].target > 0:
            cbox.pointColourRGB(i,0,255,0,point_outlines)
            cbox.update()
        else:
            cbox.pointColourRGB(i,0,0,255,point_outlines)
            cbox.update()
    else:
        print(points[i].x,points[i].y,points[i].target)
        cbox.pointColourRGB(i,255,0,0,point_outlines)
        cbox.update()
print("Correct Guesses: " + str(correct_guesses) + " / " + str(testing_size))
print("Correct Percentage: " + str(round(100 * (correct_guesses/testing_size),3)) + "%")
cbox.window.mainloop()
