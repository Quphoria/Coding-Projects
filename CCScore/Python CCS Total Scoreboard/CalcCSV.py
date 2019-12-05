import time
start = time.time()

try:
    import LiveCSV
except Exception as ex:
    print("[LiveCSV] Error: " + str(ex))
try:
    import TotalCSV
except Exception as ex:
    print("[TotalCSV] Error: " + str(ex))
try:
    import HTMLCSV
except Exception as ex:
    print("[HTMLCSV] Error: " + str(ex))

elapsed_time = (time.time() - start)

print("CSV Operations Finished. Time: {:.3f} s".format(elapsed_time))
