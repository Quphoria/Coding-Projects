from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_CONNECT(self):
        # print(self.command)
        # print(self.path)
        # print(self.headers)
        self.send_response(307)
        self.send_header('Location', "http://localhost:8080")
        self.end_headers()
    def do_GET(self):
        # print(self.command)
        # print(self.path)
        # print(self.headers)
        if (self.command == "GET" and self.path == "/truth.jpg"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(open("truth.jpg","rb").read())
        elif (self.command == "GET" and self.path == "/favicon.ico"):
            self.send_response(200)
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()
            self.wfile.write(open("favicon.ico","rb").read())
        elif (self.command == "GET" and (self.path == "/index.html" or self.path == "/")):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(open("index.html","rb").read())
        else:
            self.send_response(307)
            self.send_header('Location', "http://localhost:8080")
            self.end_headers()

def redirect(location):
    pass

server = HTTPServer(('localhost', 8080), Handler)
server.serve_forever()
