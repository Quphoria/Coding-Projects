import hashlib
def toMD5(strtohash):
    MD5Hash = hashlib.md5(strtohash.encode()).hexdigest() #Convert to MD5 Here
    return(MD5Hash)
print("String to MD5 tool")
while True:
    print()
    MD5String = toMD5(input("String: "))
    print("MD5:    " + str(MD5String))
    print()
