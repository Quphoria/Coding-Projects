var http = require('http');
var fs = require('fs');

http.createServer(function (req, res) {
  // console.log(req);
  console.log("\n----- New Request -----");
  console.log("Client:",req.headers.host);
  console.log("Method:",req.method);
  console.log("Url:",req.url);
  res.writeHead(200, {'Content-Type': 'text/html'});
  response_data = fs.readFileSync(__dirname + '/index.html', 'utf8');
  res.end(response_data);
  console.log(response_data);
}).listen(8080);

