class SmartBox:
    def __init__(self, serial_port):
        import serial
        import atexit
        def exit_handler():
            self.openConnection()
            self.writeDigital("00000000")
            self.writeMotors([0,0,0,0])
        atexit.register(exit_handler)
        self.comms = serial.Serial()
        self.comms.baudrate = 9600
        self.comms.port = serial_port
        self.motors = [0,0,0,0]
        self.outputs = [0,0,0,0,0,0,0,0]
    def port_write(self,data):
        if type(data) == int:
            data = [data]
        self.comms.write(bytes(data))
        # self.comms.flushOutput()
    def port_init(self):
        init_commmands = [[0x11,0x01],[0x14,0x00],[0x0e,0x01],[0x0e,0x02],[0x0e,0x03],[0x0e,0x04],[0x0e,0x01],[0x0e,0x02],[0x0e,0x03],[0x0e,0x04]]
        for command in init_commmands:
            self.port_write(command)
        self.motors = [0,0,0,0]
        self.outputs = [0,0,0,0,0,0,0,0]
    def openConnection(self):
        if not self.comms.is_open:
            self.comms.open()
            self.port_init()
    def readConnection(self):
        if self.comms.is_open:
            # print("READING")
            self.port_write(0x5a)
            digital_inputs = self.comms.read(1)
            self.port_write([0x2c,0x29])
            analogue_data = self.comms.read(8).hex()
            analogue_inputs = analogue_data[2:4] + analogue_data[6:8] + analogue_data[10:12] + analogue_data[14:16]
            return [format(int(digital_inputs.hex(), base=16), '#010b')[2:],analogue_inputs]
        else:
            return False
    def writeDigital(self,data):
        if self.comms.is_open:
            self.comms.write([0x14,int(data, 2)])
            return True
        else:
            return False
    def motorPower(self,power):
        if self.comms.is_open:
            self.comms.write([0x11,max(min(int(power),3),1)])
            return True
        else:
            return False
    def writeMotors(self,motordata):
        if self.comms.is_open:
            motornum = 0
            for motor in motordata:
                motornum += 1
                if motor != self.motors[motornum-1]:
                    self.motors[motornum-1] = motor
                    motorspeed = max(min(int(motor),10),-10)
                    if motorspeed == 0:
                        self.comms.write([0x0E,motornum])
                    elif motorspeed == 10:
                        self.comms.write([0x0C,motornum])
                    elif motorspeed == -10:
                        self.comms.write([0x0D,motornum])
                    else:
                        speed = abs(motorspeed)
                        inv_speed = 10 - abs(motorspeed)
                        if motorspeed > 0:
                            self.comms.write([0x0C,motornum,0x0F,motornum,speed,inv_speed])
                        elif motorspeed < 0:
                            self.comms.write([0x0D,motornum,0x0F,motornum,speed,inv_speed])
            return True
        else:
            return False
    def getInput(self):
        pass
    def getInputs(self):
        pass
    def getOutput(self):
        pass
    def getOutputs(self):
        pass
    def setOutput(self):
        pass
    def setOutputs(self):
        pass

SevenSegment = {
    ""  : "00000000",
    "0" : "00111111",
    "1" : "00000110",
    "2" : "01011011",
    "3" : "01001111",
    "4" : "01100110",
    "5" : "01101101",
    "6" : "01111101",
    "7" : "00000111",
    "8" : "01111111",
    "9" : "01100111",
    "A" : "01110111",
    "B" : "01111100",
    "C" : "00111001",
    "D" : "01011110",
    "E" : "01111001",
    "F" : "01110001"}

numorder = ["0","1","2","3","4","5","6","7","8","9","F"]
pausetime = 0.15

if __name__ == "__main__":
    import time
    port = "COM1"
    SB = SmartBox(port)
    SB.openConnection()
    disconnected = False
    outnum = 0
    motornum = 0
    SB.motorPower(3)
    motorA = 0
    speed = 0
    checktime = time.time() - pausetime
    while not disconnected:
        motor_output_status = SB.writeMotors([motorA,0,0,0])
        inputs = SB.readConnection()
        currenttime = time.time()
        if inputs and motor_output_status:
            plusone = int(inputs[0][7])
            minusone = int(inputs[0][6])
            if not plusone and not minusone:
                checktime = time.time() - pausetime
            if plusone and checktime + pausetime < currenttime:
                speed += 1
                checktime = time.time()
            if minusone and checktime + pausetime < currenttime:
                speed -= 1
                checktime = time.time()
            speed = min(max(speed,-10),10)
            letter = SevenSegment[numorder[abs(speed)]]
            if speed < 0:
                letter = "1" + letter[1:]
            SB.writeDigital(letter)
            motorA = speed



    # while not disconnected:
    #     if outnum > 8:
    #         outnum = 0
    #     if motornum > 10:
    #         motornum = -10
    #     digital_outputs = "0"
    #     if outnum > 0:
    #         digital_outputs = "1" + ("0" * (outnum - 1))
    #     # time.sleep(1)
    #     digital_output_status = SB.writeDigital(digital_outputs)
    #     motor_output_status = SB.writeMotors([motornum,motornum,motornum,motornum])
    #     inputs = SB.readConnection()
    #     if inputs and digital_output_status and motor_output_status:
    #     # print("DIGITAL INPUTS: %s" % format(int(inputs[0], base=16), '#010b'))
    #     # print("ANALOGUE INPUTS: %s" % inputs[1])
    #         print("DIGITAL INPUTS: %s  ANALOGUE INPUTS: %s" % (inputs[0],inputs[1]))
    #     else:
    #         disconnected = True
    #         print("PORT DISCONNECTED.")
    #     outnum += 1
    #     motornum += 1
