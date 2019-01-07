class Point:
    def __init__(self,calc_funct,width,height):
        import random
        self.x = random.random() * width
        self.y = random.random() * height
        # if calc_funct(self.x,self.y) >= 0:
        #     self.target = 1
        # else:
        #     self.target = -1
        self.target = calc_funct(self.x,self.y)
        self.location = [self.x,self.y]
