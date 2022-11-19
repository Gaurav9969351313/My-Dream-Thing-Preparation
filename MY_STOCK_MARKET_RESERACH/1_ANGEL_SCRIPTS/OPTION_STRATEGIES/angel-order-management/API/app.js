var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var fs = require("fs");
require('dotenv').config({path:'./.env'}) 
var { loginApi } = require('./router/angel_login.router');
var orders = require('./router/orders.router');


// loginApi()


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

//Require the Router we defined in movies.js

//Use the Router on the sub route /movies
app.use('/api/orders', orders);

var server = app.listen(7000, function () {
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