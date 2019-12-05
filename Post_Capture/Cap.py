# from scapy.all import IP, sniff, TCP
# from scapy.layers import http
# from scapy.all import *
#
#
# stars = lambda n: "*" * n
#
# def tcp_filter(packet):
#     # packet.show()
#     print(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n"))
#     # if not packet.haslayer(http.HTTPRequest):
#     #     return
#     http_request = packet.getlayer(http.HTTPRequest)
#     ip_address = packet.getlayer(IP)
#
#     if not packet.getlayer(http.HTTPRequest).Method == b'POST':
#         # print(stars(25))
#         # return('Source: {0[src]} Method: {1[Method]} Target:{1[Host]}{1[Path]}\r\n'.format(ip_address.fields, http_request.fields))
#         return
#     else:
#         print(stars(25))
#         print("POST!")
#
#         print("packet_Raw: " + str(packet[TCP].payload))
#         print("http_Fields: " + str(http_request.fields))
#         return('Source: {0[src]} Method: {1[Method]} Target: {1[Host]}{1[Path]}\r\n'.format(ip_address.fields, http_request.fields))
#
# a = sniff(filter='tcp port 80', lfilter=lambda p: "POST" in str(p), prn=tcp_filter)
# # for packet in a:
# #     if HTTPResponse in packet:
# #         packet.show()


from scapy.all import *

stars = lambda n: "*" * n

def POST_print(packet):
    return "\n".join((
        stars(40) + "POST PACKET" + stars(40),
        "\n".join(packet.sprintf("{Raw:%Raw.load%}").split(r"\r\n")),
        stars(90)))

sniff(
    prn=POST_print,
    # lfilter=lambda p: "POST" in str(p),
    filter="tcp port 80")