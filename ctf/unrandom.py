#!/usr/bin/python -u
import random,string

encflag = "BNZQ:20380043pc5p8u861tcy650q8xn8mf5d"
flag = ""
random.seed("random")
for c in encflag:
  if c.islower():
    #rotate number around alphabet a random amount
    # flag += chr((ord("a")-ord(c)-random.randrange(0,26))%26 + ord("a"))
    # flag += chr(ord(c)-ord("a")+(-random.randrange(0,26)+ord("a")))
    # flag += chr(ord(c)-97+(-random.randrange(0,26)+97))
    # flag += chr((abs(ord(c)-97-(2 * random.randrange(0,26))))%26+97)
    flag += chr(((ord(c)-ord('a'))-random.randrange(0,26))%26 + ord('a'))
    # encflag += chr((ord(c)-ord('a')+random.randrange(0,26))%26 + ord('a'))
  elif c.isupper():
    # flag += chr((abs(ord(c)-65-(2 * random.randrange(0,26))))%26+65)
    # chr((abs(ord(c)-65-(2 * random.randrange(0,26))))%26+65)

    # flag += chr((ord("A")-ord(c)-random.randrange(0,26))%26 + ord("A"))
    # encflag += chr((ord(c)-ord('A')+random.randrange(0,26))%26 + ord('A'))
    flag += chr(((ord(c)-ord('A'))-random.randrange(0,26))%26 + ord('A'))
    # encflag += chr((ord(c)-65+random.randrange(0,26))%26 + 65)
  elif c.isdigit():
    # flag += chr((abs(ord(c)-48-(2 * random.randrange(0,10))))%10+48)
    flag += chr(((ord(c)-ord('0'))-random.randrange(0,10))%10 + ord('0'))
    # flag += chr(ord(c)-ord("0")+(-random.randrange(0,10)+ord("0")))
    # flag += chr((ord("0")-ord(c)-random.randrange(0,10))%10 + ord("0"))
    #encflag += chr((ord(c)-ord('0')+random.randrange(0,10))%10 + ord('0'))
  else:
    flag += c
    # encflag += c
print("Flag: "+flag)
