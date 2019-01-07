from __future__ import print_function

import os, sys, check_update, os.path

conf_template = """{
  "ConfigFile" : "dns.json",
  "Origin" : ".",
  "TTL" : "60s",
  "Port" : 53,
  "Address" : "",

  "TCP" : false,
  "Log" : "request,truncated",
  "Log Prefix" : true,
  "Upstream DNS Server" : "192.168.1.1:53",
  "Upstream DNS Timeout" : 5,
  "logfile":"Logs\\\\dns.log",
  "old-logfile":"Logs\\\\Old\\\\dns.log",
  "NSSM":"NSSM\\\\nssm.exe"
}"""
dns_template = """{
  "example.com" : {
    "127.0.0.1" : ["127.0.0"]
  }
}"""


script_path = os.path.dirname(os.path.realpath(sys.argv[0]))

# os.system("\"\"%s\\python.exe\"\" -m http.server 8888" % script_path)
from multiprocessing import Process

def hprocess():
    import http.server, socketserver
    class handler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            mimetype = self.guess_type(self.path)
            is_file = not self.path.endswith('/')
            if is_file and mimetype in ['text/plain', 'application/octet-stream']:
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Content-Disposition', 'inline')
            super().end_headers()
        def log_error(self, *args):
            pass
        def log_message(self, *args):
            pass
        def log_request(self, *args):
            pass
        def log_date_time_string(self, *args):
            pass
    httpd = socketserver.TCPServer(("",8888), handler)
    httpd.serve_forever()
p = Process(target=hprocess)

hserv = True

import socket

try:
    from subprocess import getoutput
except ImportError:
    from commands import getoutput

from dnslib import RR,QTYPE,RCODE,A,parse_time
from dnslib.label import DNSLabel
from dnslib.server import DNSServer,DNSHandler,BaseResolver,DNSRecord

class DNSLogger:
    def __init__(self,log="",prefix=True):
        """
            Selectively enable log hooks depending on log argument
            (comma separated list of hooks to enable/disable)

            - If empty enable default log hooks
            - If entry starts with '+' (eg. +send,+recv) enable hook
            - If entry starts with '-' (eg. -data) disable hook
            - If entry doesn't start with +/- replace defaults

            Prefix argument enables/disables log prefix
        """
        default = ["request","reply","truncated","error"]
        log = log.split(",") if log else []
        enabled = set([ s for s in log if s[0] not in '+-'] or default)
        [ enabled.add(l[1:]) for l in log if l.startswith('+') ]
        [ enabled.discard(l[1:]) for l in log if l.startswith('-') ]
        for l in ['log_recv','log_send','log_request','log_reply',
                  'log_truncated','log_error','log_data']:
            if l[4:] not in enabled:
                setattr(self,l,self.log_pass)
        self.prefix = prefix
        import datetime
        self.datetime = datetime

    def log_pass(self,*args):
        pass

    def log_prefix(self,handler):
        if self.prefix:
            return "[%s] " % self.datetime.datetime.now()
        else:
            return ""

    def log_recv(self,handler,data):
        Log("%sReceived: [%s:%d] <%d> : %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    len(data),
                    binascii.hexlify(data)))

    def log_send(self,handler,data):
        Log("%sSent: [%s:%d] <%d> : %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    len(data),
                    binascii.hexlify(data)))

    def log_request(self,handler,request):
        Log("%sRequest: [%s:%d] / '%s' (%s)" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    request.q.qname,
                    QTYPE[request.q.qtype]))
        self.log_data(request)

    def log_reply(self,handler,reply):
        if reply.header.rcode == RCODE.NOERROR:
            Log("%sReply: [%s:%d] / '%s' (%s) / RRs: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr])))
        else:
            Log("%sReply: [%s:%d] / '%s' (%s) / %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    RCODE[reply.header.rcode]))
        self.log_data(reply)

    def log_truncated(self,handler,reply):
        Log("%sTruncated Reply: [%s:%d] / '%s' (%s) / RRs: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr])))
        self.log_data(reply)

    def log_error(self,handler,e):
        Log("%sInvalid Request: [%s:%d] :: %s" % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    e))

    def log_data(self,dnsobj):
        Log("{%s} \n%s\n" % (self.datetime.datetime.now(), dnsobj.toZone("    ")))

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
    if hserv:
        p.start()

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

    LogFileName = confdata["logfile"]
    TLogFileName = confdata["old-logfile"].rsplit(".",1)[0] + " @ " + check_update.LoadTime + "." + confdata["old-logfile"].rsplit(".",1)[1]
    if os.path.exists(LogFileName):
        try:
            os.remove(LogFileName)
        except:
            pass

    def Log(text="",end="\r\n"):
        if not os.path.exists(os.path.split(confdata["old-logfile"])[0]):
            os.mkdir(os.path.split(confdata["old-logfile"])[0])
        #sys.stdout.write((("%s" % text) + end))
        #sys.stdout.flush()
        LogFile = open(LogFileName,"ab")
        LogFile.write((("%s" % text) + end).encode())
        LogFile.close()
        LogFile = open(TLogFileName,"ab")
        LogFile.write((("%s" % text) + end).encode())
        LogFile.close()

    Log("DNS Server started at %s" % check_update.LoadTime)
    Log("Python DNS Server version %s" % check_update.dns_version())
    Log("Using json file: %s" % jsonfilename)

    Log(jsondata.keys())
    domains = jsondata.keys()
    for domain in domains:
        Log("Domain: %s" % domain)
        Log("IP Zones:")
        for i in jsondata[domain]:
            ipstring = ""
            for j in jsondata[domain][i]:
                ipstring += ", %s.*" % j
            ipstring = ipstring[1:]
            Log("IP range:%s | Zone IP: %s" % (ipstring, i))
        Log()

    import sys,time,datetime

    dns,_,dns_port = confdata["Upstream DNS Server"].partition(':')
    if dns_port == "":
        dns_port = 53
    resolver = DNSResolver(jsondata,confdata["Origin"],confdata["TTL"],dns,int(dns_port),confdata["Upstream DNS Timeout"])
    logger = DNSLogger(confdata["Log"],confdata["Log Prefix"])

    Log("Starting DNS Resolver (%s:%d) [%s]" % (
                        confdata["Address"] or "*",
                        confdata["Port"],
                        "UDP/TCP" if confdata["TCP"] else "UDP"))

    for route,cmd in resolver.routes.items():
        Log("    |  %s --> %s" % (route, cmd))
    Log()

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

    updatetimer = 710
    timerestart = False
    restarttimer = 0
    while udp_server.isAlive():
        time.sleep(1)
        updatetimer += 1
        if timerestart:
            restarttimer += 1
            updatetimer = 0
            if restarttimer == 60:
                pid_file = open(pid_filename,"w")
                pid_file.write("-1")
                pid_file.close()
        if updatetimer > 720:
            updatetimer = 0
            check_update.check_for_update()
        pid_filename = script_path + "\dns.pid"
        pid_file = open(pid_filename,"r")
        pid_file_value = pid_file.read()
        pid_file.close()
        now = datetime.datetime.now()
        if now.hour == 23 and now.minute == 59 and not timerestart:
            Log("DNS Server restarting in 1 minute!")
            timerestart = True
        if pid != int(pid_file_value):
            if int(pid_file_value) == -1:
                Log("Restarting Service...")
            p.terminate()
            time.sleep(0.1)
            if not p.is_alive():
                p.join(timeout=1.0)
            Log()
            Log()
            sys.exit()
