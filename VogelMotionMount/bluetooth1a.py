import asyncio
from bleak import BleakClient
import threading
from termcolor import colored

print("V1")

presets = [[bytearray(4), b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"], [bytearray(4), b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"]]
preset_labels = ["Wall", "College Hall", "Chapel"]
# print(presets)
displays = ["Left","Right"]
displays_print = ["Left ", "Right"]
addresses = ['34:15:13:d0:58:e2','34:15:13:d0:48:9e']
threads = []

# c0:05:fa:21:06:51:48:00:b0:00:00:00:00:00:00:00
write_uuid = "c005fa21-0651-4800-b000-000000000000"
swivel_notify_uuid = "c005fa01-0651-4800-b000-000000000000"
distance_notify_uuid = "c005fa00-0651-4800-b000-000000000000"

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

# def start_loop(loop):
#     asyncio.set_event_loop(loop)
#     loop.run_forever()
# new_loop = asyncio.new_event_loop()
# t = threading.Thread(target=start_loop, args=(new_loop,))
# t.start()

class BTThread(threading.Thread):
    def __init__(self, address, _presets):
        threading.Thread.__init__(self)
        self.address = address
        self.presets = _presets
        self.command_list = []
    def run(self):
        print(colored("Started Thread " + address, 'cyan'))
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.run_bleak(loop))
        # asyncio.run_coroutine_threadsafe(run_bleak(self),loop)
        print(colored("Stopped Thread " + address, 'cyan'))

    async def run_bleak(self, loop):
        def swivel_notify_callback(sender, data):
            print(colored("[" + displays_print[addresses.index(sender)] + "] :S: " + str(data), 'grey'))
        def distance_notify_callback(sender, data):
            print(colored("[" + displays_print[addresses.index(sender)] + "] :D: " + str(data), 'grey'))

        exitFlag = False
        while not exitFlag:
            print(colored("Connecting to [" + self.address + "]...", 'yellow'))
            try:
                async with BleakClient(self.address, loop=loop) as client:
                    print(colored("Connected to [" + self.address + "]", 'green'))
                    await asyncio.sleep(5, loop=client.loop)
                    await client.start_notify(swivel_notify_uuid, swivel_notify_callback)
                    await client.start_notify(distance_notify_uuid, distance_notify_callback)
                    while not exitFlag and await client.is_connected():
                        await asyncio.sleep(1, loop=client.loop)
                        if len(self.command_list) > 0:
                            command_id = self.command_list.pop(0)
                            if command_id != -1:
                                command = presets[command_id]
                                print(colored("[" + self.address + "] Sending...", 'green'))
                                await client.write_gatt_char(write_uuid, command)
                            else:
                                exitFlag = True
            except Exception as ex:
                print(colored("[" + self.address + "] An Error Occurred: " + str(ex), 'red'))

threadnum = 0
for address in addresses:
    thread = BTThread(address, presets[threadnum])
    thread.daemon = True
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
