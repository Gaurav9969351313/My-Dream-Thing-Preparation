var express = require('express');
var app = express();
var fs = require("fs");
require('dotenv').config({path:'./.env'}) 
var axios = require('axios');
var { SmartAPI, WebSocket } = require("smartapi-javascript");
// var { loginApi, getLtp, getRMS, getOrderBook } = require('./angel');

// loginApi()

var server = app.listen(8081, function () {
    var host = server.address().address
    var port = server.address().port
    console.log("App listening at http://%s:%s", host, port)
 })


// keshav nagar
// mundhava
// yerwda 
// kalyani nagar 
// kharadi
// logoan
// Hadapsar