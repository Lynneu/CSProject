'use strict';

// a simple http server

var
    fs = require('fs'),
    url = require('url'),
    path = require('path'),
    http = require('http');

var root = path.resolve(process.argv[2] || '.');

console.log('Static root dir: ' + root);

var server = http.createServer(function (request, response) {
    var
        pathname = url.parse(request.url).pathname, // '/static/bootstrap.css'
        filepath = path.join(root, pathname); // '/srv/www/static/bootstrap.css'
    fs.stat(filepath, function (err, stats) {
        if (!err && stats.isFile()) {
            console.log('200 ' + request.url);
            response.writeHead(200);
            fs.createReadStream(filepath).pipe(response);
        }
        else if(!err && stats.isDirectory()){
            filepath = path.join(filepath,'in.html');
            fs.stat(filepath, function(err, stats){
                if (!err && stats.isFile()) {
                    console.log('200 ' + request.url);
                    response.writeHead(200);
                    fs.createReadStream(filepath).pipe(response);
                }
                else {
                    filepath = path.dirname(firepath);
                    filepath = path.join(filepath,'default.html');
                    fs.stat(filepath, function(err, stats){
                        if (!err && stats.isFile()) {
                            console.log('200 ' + request.url);
                            response.writeHead(200);
                            fs.createReadStream(filepath).pipe(response);
                        }
                        else{
                            console.log('404 ' + request.url);
                            response.writeHead(404);
                            response.end('404 Not Found');
                        }
                    });
                }
            });

        } 
        else {
            console.log('404 ' + request.url);
            response.writeHead(404);
            response.end('404 Not Found');
        }
    });
});

server.listen(7070);

console.log('Server is running at http://127.0.0.1:7070/');