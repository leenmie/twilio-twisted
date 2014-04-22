/*
 * Just a proxy for a quick test
 */

var http = require('http'),
    httpProxy = require('http-proxy');
httpProxy.createProxyServer({target:'https://api.twilio.com'}).listen(9999);
