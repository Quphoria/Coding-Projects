try:
    from b import run
    global value
    value = "Variable Success!"
    run()
except Exception as ex:
    print("An error occurred: " + str(ex))
input()
