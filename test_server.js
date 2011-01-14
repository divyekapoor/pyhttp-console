var http = require('http');
var util = require('util');


var httpServer = http.Server();
httpServer.on('request', function(req, resp) {
    util.log(req.method + ' ' + req.url);
    resp.writeHead(200, {'content-type':'text/plain'});

    if(req.method !== "HEAD") {
        resp.write('Method: ' + req.method + '\nUrl: ' + req.url + '\nHeaders:\n' + util.inspect(req.headers, true, null) + '\nData: \n');

        req.on('data', function(chunk) { 
            resp.write(chunk);
        });
    }

    req.on('end', function() { 
        resp.end();
    });

});

httpServer.listen(8090, '127.0.0.1', function() {
    console.log('Server started on http://localhost:8090');
});

