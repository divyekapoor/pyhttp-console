#!/usr/bin/env node
//
//          Copyright Divye Kapoor 2010
// Distributed under the Boost Software License, Version 1.0.
//    (See accompanying file LICENSE_1_0.txt or copy at
//          http://www.boost.org/LICENSE_1_0.txt) 
//
//
// This file is a Node.js based HTTP Server that's useful for testing
// It echoes back the http request method, the request url, request headers
// and request body.
//

var http = require('http');
var util = require('util');


var httpServer = http.Server();
httpServer.on('request', function(req, resp) {

    util.log(req.method + ' ' + req.url); // Keep a timestamped log of requests made to the server

    resp.writeHead(200, {'content-type':'text/plain'});

    if(req.method !== "HEAD") { // No response body allowed for HEAD requests as per HTTP RFC.
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

