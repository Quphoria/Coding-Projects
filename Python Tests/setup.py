from cx_Freeze import setup, Executable

base = None

inputfile = input("Python File: ")

executables = [Executable(inputfile, base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "<any name>",
    options = options,
    #version = "<any number>",
    version = "1",
    description = '<any description>',
    executables = executables
)
