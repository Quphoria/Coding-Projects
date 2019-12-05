import pygatt
import time, threading
from termcolor import colored

print("V2")

presets = [[b"\x00\x00\x00\x00", b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"], [b"\x00\x00\x00\x00", b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"]]
preset_labels = ["Wall", "College Hall", "Chapel"]
# print(presets)
displays = ["Left","Right"]
displays_print = ["Left ", "Right"]
addresses = ['34:15:13:d0:58:e2','34:15:13:d0:48:9e']
threads = []

# c0:05:fa:21:06:51:48:00:b0:00:00:00:00:00:00:00
write_uuid = "c005fa21-0651-4800-b000-000000000000"

def take_input():
    valid = False
    display = -1
    for i in range(len(displays)):
        print(str(i) + ": " + displays[i])
    while not valid:
        display_input = input("Display: ")
        if display_input in ["0","1"]:
            display = int(display_input)
            valid = True
        elif display_input == "quit":
            valid = True

    for i in range(len(preset_labels)):
        print(str(i) + ": " + preset_labels[i])
    valid = False
    preset = -1
    while not valid:
        preset_input = input("Preset: ")
        if preset_input in ["0","1","2"]:
            preset = int(preset_input)
            valid = True
        elif preset_input == "quit":
            valid = True
    return display, preset

class BTThread(threading.Thread):
    def __init__(self, address, _presets):
        threading.Thread.__init__(self)
        self.address = address
        self.presets = _presets
        self.command_list = []
    def run(self):
        print(colored("Started Thread " + self.address, 'cyan'))
        adapter = pygatt.GATTToolBackend()
        exitFlag = False
        while not exitFlag:
            print(colored("Connecting to [" + self.address + "]...", 'yellow'))
            adapter.start()
            try:
                # services = bluetooth.find_service(uuid=write_uuid, address=self.address)
                device = adapter.connect(self.address)
                tries = 0
                while tries < 20 and len(services) == 0:
                    time.sleep(1)
                    device = adapter.connect(self.address)
                    tries += 1
                    print(tries)
                print(colored("Connected to [" + self.address + "]", 'green'))
                time.sleep(3)
                while not exitFlag:
                    rssi = device.get_rssi()
                    if rssi == None:
                        exitFlag = True
                    else:
                        print(colored("[" + self.address + "] RSSI: " + str(rssi), 'grey'))
                    time.sleep(3)
                    if len(self.command_list) > 0 and not exitFlag:
                        command_id = self.command_list.pop(0)
                        if command_id != -1:
                            # send command
                            try:
                                command = presets[command_id]
                                device.char_write(write_uuid, command)
                            except Exception as ex:
                                print("Send Error: " + str(ex))
                        else:
                            exitFlag = True
            except Exception as ex:
                print(colored("[" + self.address + "] An Error Occurred: " + str(ex), 'red'))
        print(colored("Stopped Thread " + self.address, 'cyan'))

threadnum = 0
for address in addresses:
    thread = BTThread(address, presets[threadnum])
    thread.start()
    threads.append(thread)
    threadnum += 1

while True:
    input("Press enter to send a command: ")
    display, preset = take_input()
    if display == -1:
        break
    if preset == -1:
        break

    threads[display].command_list.append(preset)
for thread in threads:
    thread.command_list.append(-1)
    thread.join()
