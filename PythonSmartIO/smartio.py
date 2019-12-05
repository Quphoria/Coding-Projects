from smartbox import SmartBox
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
    while not disconnected:
        if outnum > 8:
            outnum = 0
        if motornum > 10:
            motornum = -10
        digital_outputs = "0"
        if outnum > 0:
            digital_outputs = "1" + ("0" * (outnum - 1))
        # time.sleep(1)
        digital_output_status = SB.writeDigital(digital_outputs)
        motor_output_status = SB.writeMotors([motornum,motornum,motornum,motornum])
        inputs = SB.readConnection()
        if inputs and digital_output_status and motor_output_status:
        # print("DIGITAL INPUTS: %s" % format(int(inputs[0], base=16), '#010b'))
        # print("ANALOGUE INPUTS: %s" % inputs[1])
            print("DIGITAL INPUTS: %s  ANALOGUE INPUTS: %s" % (inputs[0],inputs[1]))
        else:
            disconnected = True
            print("PORT DISCONNECTED.")
        outnum += 1
        motornum += 1