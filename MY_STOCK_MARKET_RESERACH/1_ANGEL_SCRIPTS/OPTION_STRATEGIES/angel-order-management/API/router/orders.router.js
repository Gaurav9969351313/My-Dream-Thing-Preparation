var express = require('express');
var axios = require('axios');

var router = express.Router();
// var { getTradeBook } = require('../angel');

function getHeaders(isWithJWTToken) {
    if (isWithJWTToken == "Y") {
        return {
            'Authorization': 'Bearer ' + global.jwtToken,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-PrivateKey': process.env.API_KEY
        }

    } else if (isWithJWTToken == "N") {
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-UserType': 'USER',
            'X-SourceID': 'WEB',
            'X-ClientLocalIP': 'CLIENT_LOCAL_IP',
            'X-ClientPublicIP': 'CLIENT_PUBLIC_IP',
            'X-MACAddress': 'MAC_ADDRESS',
            'X-PrivateKey': process.env.API_KEY
        }
    }
}

// it provides the trades for the current day
router.get('/getTradeBook', async function(req, res){
    var data = {};
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOrderBook',
        headers: getHeaders("Y"),
        data: data
    };

    await axios(config)
        .then(function (response) {
            res.json(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
});

router.get('/getRMS', async function(req, res){
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getRMS',
        headers: getHeaders("Y"),
    };

    await axios(config)
        .then(function (response) {
            res.json(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
});

//Get Order Book Status Response 
router.get('/getOrderBook', async function(req, res){
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOrderBook',
        headers: getHeaders("Y"),
        data: {}
    };
    await axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error.message);
        });
});

// Get Postions 
router.get('/getPosition', async function(req, res){
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getPosition',
        headers: getHeaders("Y")
    };

    axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
});

router.get('/getHoldings', async function(req, res){
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/portfolio/v1/getHolding',
        headers: getHeaders("Y")
    };

    axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
});

getLtp = () => {
    var data = JSON.stringify({
        "exchange": "NSE",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getLtpData',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

// ######################################## Order Management Starts Here ##########################################

// {
// 	"variety":"STOPLOSS",
// 	"tradingsymbol":"ACC29JUL212040CE",
// 	"symboltoken":"54341",
// 	"transactiontype":"SELL",
// 	"exchange":"NFO",
// 	"ordertype":"STOPLOSS_MARKET",
// 	"producttype":"INTRADAY",
// 	"duration":"DAY",
// 	"price":"0",
//  "triggerprice":"32",
// 	"squareoff":"0",
// 	"stoploss":"0",
// 	"quantity":"500"
// }

// lets place order for perticular exchange
router.get('/placeOrder', async function(req, res){
    var data = JSON.stringify({
        "variety": "NORMAL",
        "tradingsymbol": res.body["tradingsymbol"],
        "symboltoken": res.body["symboltoken"],
        "transactiontype": res.body["transactiontype"],
        "exchange": res.body["exchange"],
        "ordertype": res.body["ordertype"],
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": res.body["price"],
        "squareoff": "0",
        "stoploss": res.body["stoploss"],
        "quantity": res.body["quantity"]
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/placeOrder',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
});

// modify order 
router.get('/modifyOrder', async function(req, res){
    var data = JSON.stringify({
        "variety": "NORMAL",
        "orderid": req.body["orderid"],
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": req.body["price"],
        "quantity": req.body["quantity"],
        "tradingsymbol": req.body["tradingsymbol"],
        "symboltoken": req.body["symboltoken"],
        "exchange": req.body["exchange"]
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/modifyOrder',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });

});

// cancel order
router.get('/cancelOrder', async function(req, res){
    var data = JSON.stringify({
        "variety": "NORMAL",
        "orderid": req.body["orderid"]
    });  

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/cancelOrder',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            res.json(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
});

module.exports = router;