from __future__ import print_function

import os, sys, check_update, os.path

conf_template = """{
  "ConfigFile" : "dns.json",
  "Origin" : ".",
  "TTL" : "60s",
  "Port" : 53,
  "Address" : "",
  "TCP" : false,
  "Log" : "request,reply,truncated,error",
  "Log Prefix" : false,
  "Upstream DNS Server" : "192.168.1.1:53",
  "Upstream DNS Timeout" : 5
}"""
dns_template = """{
  "example.com" : {
    "127.0.0.1" : ["127.0.0"]
  }
}"""


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

pid = os.getpid()
pid_filename = script_path + "\dns.pid"
try:
    pid_file = open(pid_filename,"r")
    old_pid = pid_file.read()
    pid_file.close()
    try:
        os.kill(int(old_pid), signal.SIGTERM)
    except:
        pass
except:
    pass
pid_file = open(pid_filename,"w")
pid_file.write(str(pid))
pid_file.close()


import json

conffilename = "%s\conf.json" % script_path
if (not os.path.isfile(conffilename)):
    conffile = open(conffilename,"w")
    conffile.write(conf_template)
    conffile.close()
conffile = open(conffilename,"r")
confdata = json.load(conffile)
conffile.close()

jsonfilename = script_path + "\\" + confdata["ConfigFile"]
if (not os.path.isfile(jsonfilename)):
    jsonfile = open(jsonfilename,"w")
    jsonfile.write(dns_template)
    jsonfile.close()
jsonfile = open(jsonfilename,"r")
jsondata = json.load(jsonfile)
jsonfile.close()

print("Using json file: %s" % jsonfilename)

print(jsondata.keys())
domains = jsondata.keys()
for domain in domains:
    print("Domain: %s" % domain)
    print("IP Zones:")
    for i in jsondata[domain]:
        ipstring = ""
        for j in jsondata[domain][i]:
            ipstring += ", %s.*" % j
        ipstring = ipstring[1:]
        print("IP range:%s | Zone IP: %s" % (ipstring, i))
    print()

import socket

try:
    from subprocess import getoutput
except ImportError:
    from commands import getoutput

from dnslib import RR,QTYPE,RCODE,A,parse_time
from dnslib.label import DNSLabel
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSLogger,DNSRecord

class DNSResolver(BaseResolver):
    def __init__(self,jsondata,origin,ttl,address,port,timeout=0):
        self.origin = DNSLabel(origin)
        self.ttl = parse_time(ttl)
        self.jsondata = jsondata
        self.address = address
        self.port = port
        self.timeout = timeout
        self.routes = {}
        self.domains = jsondata.keys()
        for domain in self.domains:
            route = self.origin.add(domain)
            self.routes[route] = True
        # for r in routes:
        #     route,_,cmd = r.partition(":")
        #     if route.endswith('.'):
        #         route = DNSLabel(route)
        #     else:
        #         route = self.origin.add(route)
        #     self.routes[route] = cmd

    def resolve(self,request,handler):
        client_address = handler.client_address
        subnet = '.'.join(client_address[0].split('.')[:3])
        reply = request.reply()
        qname = request.q.qname
        rt = self.routes.get(qname)
        dnsip = ""
        if rt:
            for i in jsondata[str(qname)[:-1]]:
                if subnet in jsondata[str(qname)[:-1]][i]:
                    dnsip = i
        if rt and dnsip != "":
            reply.add_answer(RR(qname,QTYPE.A,ttl=self.ttl,
                                rdata=A(dnsip)))
        else:
            try:
                if handler.protocol == 'udp':
                    proxy_r = request.send(self.address,self.port,
                                    timeout=self.timeout)
                else:
                    proxy_r = request.send(self.address,self.port,
                                    tcp=True,timeout=self.timeout)
                reply = DNSRecord.parse(proxy_r)
            except socket.timeout:
                reply = request.reply()
                reply.header.rcode = getattr(RCODE,'NXDOMAIN')
        return reply

if __name__ == '__main__':

    import sys,time

    dns,_,dns_port = confdata["Upstream DNS Server"].partition(':')
    if dns_port == "":
        dns_port = 53
    resolver = DNSResolver(jsondata,confdata["Origin"],confdata["TTL"],dns,int(dns_port),confdata["Upstream DNS Timeout"])
    logger = DNSLogger(confdata["Log"],confdata["Log Prefix"])

    print("Starting Shell Resolver (%s:%d) [%s]" % (
                        confdata["Address"] or "*",
                        confdata["Port"],
                        "UDP/TCP" if confdata["TCP"] else "UDP"))

    for route,cmd in resolver.routes.items():
        print("    | ",route,"-->",cmd)
    print()

    udp_server = DNSServer(resolver,
                           port=confdata["Port"],
                           address=confdata["Address"],
                           logger=logger)
    udp_server.start_thread()

    if confdata["TCP"]:
        tcp_server = DNSServer(resolver,
                               port=confdata["Port"],
                               address=confdata["Address"],
                               tcp=True,
                               logger=logger)
        tcp_server.start_thread()

    updatetimer = 1790
    while udp_server.isAlive():
        time.sleep(1)
        updatetimer += 1
        if updatetimer > 1800:
            updatetimer = 0
            check_update.check_for_update()
        pid_filename = script_path + "\dns.pid"
        pid_file = open(pid_filename,"r")
        pid_file_value = pid_file.read()
        pid_file.close()
        if pid != int(pid_file_value):
            sys.exit()
