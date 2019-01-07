from kulka import Kulka
from random import randint
import time

class HSV:
    def __init__(self,hue,saturation,value):
        import colorsys
        self.h = hue
        self.s = saturation
        self.v = value
        rgb = colorsys.hsv_to_rgb(self.h/255, self.s/255, self.v/255)
        self.r = round(rgb[0] * 255)
        self.g = round(rgb[1] * 255)
        self.b = round(rgb[2] * 255)

class ArrowKeys:
    def __init__(self):
        import pygame
        self.pygame = pygame
        self.a1 = 0
        self.a2 = 0
        pygame.init()
        pygame.display.set_caption("Sphero2.0")
        screen = pygame.display.set_mode((250,50))
    def updateInputs(self):
        keys = self.pygame.key.get_pressed()
        # print(keys)
        if keys[self.pygame.K_UP]:
            self.a1 += 2
        if keys[self.pygame.K_DOWN]:
            self.a1 -= 2
        if keys[self.pygame.K_LEFT]:
            self.a2 -= 2
        if keys[self.pygame.K_RIGHT]:
            self.a2 += 2
        self.a1 = min(255,max(0,self.a1))
        if self.a2 > 359:
            self.a2 = self.a2 - 360
        if self.a2 < 0:
            self.a2 = self.a2 + 360
        self.a2 = min(359,max(0,self.a2))

class Sphero:
    def __init__(self,mac_address):
        import threading
        self.t = threading.Thread(target=control_surface,args=(mac_address,1))
        self.threading = threading
        self.reset_init()

    def set_back_led(self,level):
        globals()["Sphero_blackled"] = level
    def set_rgb(self,red,green,blue):
        globals()["Sphero_red"] = red
        globals()["Sphero_green"] = green
        globals()["Sphero_blue"] = blue
    def roll(self,a1,a2,state=1):
        globals()["Sphero_a1"] = a1
        globals()["Sphero_a2"] = a2
        globals()["Sphero_state"] = state
    def sleep(self):
        globals()["Sphero_sleep"] = True
        self.t.join()
    def start(self):
        self.t.start()
        import time
        while (not globals()["Sphero_conn"]) and self.t.is_alive():
            time.sleep(0.1)
        return globals()["Sphero_conn"]
    def stop(self):
        globals()["Sphero_stop"] = True
        self.t.join()
    def alive(self):
        return globals()["Sphero_conn"] and self.t.is_alive()
    def reset(self):
        self.stop()
        self.reset_init()
    def reset_init(self):
        globals()["Sphero_blackled"] = 0
        globals()["Sphero_red"] = 0
        globals()["Sphero_green"] = 0
        globals()["Sphero_blue"] = 0
        globals()["Sphero_sleep"] = False
        globals()["Sphero_stop"] = False
        globals()["Sphero_a1"] = 0
        globals()["Sphero_a2"] = 0
        globals()["Sphero_state"] = 1
        globals()["Sphero_h"] = 0
        globals()["Sphero_conn"] = False


def control_surface(dev_mac,timeout=3600,*args):
    old_backled = ""
    old_red = ""
    old_green = ""
    old_blue = ""
    old_a1 = ""
    old_a2 = ""
    old_h = ""
    old_state = ""
    print("Connecting to Sphero2.0...",end="",flush=True)
    with Kulka(dev_mac) as kulka:
        globals()["Sphero_conn"] = True
        print("Connected.")
        kulka.set_inactivity_timeout(timeout)
        Awake = True
        while Awake:
            if globals()["Sphero_blackled"] != old_backled:
                old_backled = globals()["Sphero_blackled"]
                kulka.set_back_led(old_backled)
            if globals()["Sphero_red"] != old_red or globals()["Sphero_green"] != old_green or globals()["Sphero_blue"] != old_blue:
                old_red = globals()["Sphero_red"]
                old_green = globals()["Sphero_green"]
                old_blue = globals()["Sphero_blue"]
                kulka.set_rgb(old_red,old_green,old_blue)
            if globals()["Sphero_h"] != old_h:
                old_h = globals()["Sphero_h"]
                kulka.set_heading(old_h)
            if globals()["Sphero_a1"] != old_a1 or globals()["Sphero_a2"] != old_a2 or globals()["Sphero_state"] != old_state:
                old_a1 = globals()["Sphero_a1"]
                old_a2 = globals()["Sphero_a2"]
                old_state = globals()["Sphero_state"]
                kulka.roll(old_a1,old_a2,old_state)
            if globals()["Sphero_sleep"]:
                Awake = False
                kulka.sleep()
            if globals()["Sphero_stop"]:
                Awake = False
    globals()["Sphero_conn"] = True


AK = ArrowKeys()


SP = Sphero('68:86:E7:03:4A:B6')
connected = SP.start()
if connected:
    SP.set_back_led(255)
    running = True
    while (running):
        for event in AK.pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == AK.pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
        if not SP.alive():
            running = False
        AK.updateInputs()
        # a1 = randint(0, 255)
        # a2 = randint(0, 359)
        a1 = AK.a1
        a2 = AK.a2
        print((a1,a2))
        SP.roll(a1,a2)
        rgb = HSV(round(255*(a2/359)),a1,255)
        SP.set_rgb(rgb.r, rgb.g, rgb.b)
        # time.sleep(2)
        time.sleep(0.02)
    SP.sleep()
