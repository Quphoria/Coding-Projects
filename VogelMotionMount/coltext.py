from termcolor import colored

print(colored('hello', 'red'), colored('world', 'green'))
presets = [[b"\x00\x00\x00\x00", b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"], [b"\x00\x00\x00\x00", b"\x00\x64\x00\x64", b"\x00\x64\xff\x9c"]]
preset = presets[0][2]
print(type(preset))
print(preset)
bt = bytes(preset)
print(type(bt))
print(bt)
