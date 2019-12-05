import logging
logging.getLogger("scapy").setLevel(1)

from scapy.all import *

def make_test(x,y):
    request = "GET / HTTP/1.1\r\nHost: " + y  + "\r\n"
    p = IP(dst=x)/TCP()/request
    out = sr1(p)
    if out:
        out.show()
if __name__ == "__main__":
    interact(mydict=globals(), mybanner="Scapy HTTP Tester")