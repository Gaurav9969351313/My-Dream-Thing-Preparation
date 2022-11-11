var axios = require('axios');
const totp = require("totp-generator");
const token = totp(process.env.TOTP_TOKEN);

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

exports.getHeaders = () => {
    return getHeaders("Y")
}

exports.loginApi = () => {
    var data = JSON.stringify({
        "clientcode": process.env.CLIENT_CODE,
        "password": process.env.CLIENT_PASSWORD,
        "totp": token
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword',
        headers: getHeaders("N"),
        data: data
    };

    axios(config)
        .then(function (response) {
            global.jwtToken = response.data.data["jwtToken"];
            console.log("====================== Login Successful ======================");
        })
        .then(()=>{
            // getProfile()
            // getLtp()
            // getRMS()
            // getOrderBook()
        })
        .catch(function (error) {
            console.log(error.errorCode);
        });
}

getProfile = () => {
    var head = getHeaders("Y");
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getProfile',
        headers: head
    };
    console.log(head);
    axios(config)
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

getRMS = () => {
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/getRMS',
        headers: getHeaders("Y"),
    };

    axios(config)
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error);
        });
}

exports.logout = () => {
    var data = JSON.stringify({
        "clientcode": process.env.CLIENT_CODE
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/user/v1/logout',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });
}

// ######################################## Order Management Starts Here ##########################################

//Get Order Status Response 
getOrderBook = () => {
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOrderBook',
        headers: getHeaders("Y"),
        data: {}
    };
    axios(config)
        .then(function (response) {
            console.log(response.data);
        })
        .catch(function (error) {
            console.log(error.message);
        });
}

// it provides the trades for the current day
getTradeBook = () => {
    var data = {};
    var config = {
        method: 'get',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOrderBook',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });
}

// last trade price or perticuler exchange 
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

// lets place order for perticular exchange
exports.placeOrder = () => {
    var data = JSON.stringify({
        "variety": "NORMAL",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "MARKET",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "194.50",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": "10"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/placeOrder',
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

// modify order 
exports.modifyOrder = () => {
    var data = JSON.stringify({
        "variety": "NORMAL",
        "orderid": "220408001053631",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "194.00",
        "quantity": "55",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "exchange": "NSE"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/modifyOrder',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });

}

// cancel order
exports.cancelOrder = () => {
    var data = JSON.stringify({
        "variety": "NORMAL",
        "orderid": "220408001019071"
    });  

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/cancelOrder',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });
}

// ############################################# GTT ###############################################

var axios = require('axios');


// generate rule
exports.genrateRule = () => {
    var data = JSON.stringify({
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045", 
        "exchange": "NSE", 
        "transactiontype": "BUY",
        "producttype": "DELIVERY", 
        "price": "10", 
        "qty": "5",
        "triggerprice": "10", 
        "disclosedqty": "1", 
        "timeperiod": "20"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/gtt/v1/createRule',
        headers: getHeaders("Y"),
        data: data
    };

    axios(config)
        .then(function (response) {
            console.log(JSON.stringify(response.data));
        })
        .catch(function (error) {
            console.log(error);
        });
}



// modify genrated rule by id
exports.modifyRule = () => {
    var data = JSON.stringify({
        "id": "5130853", 
        "symboltoken": "3045",
        "exchange": "NSE", 
        "price": "20", 
        "qty": "60",
        "triggerprice": "20", 
        "disclosedqty": "10", 
        "timeperiod": "20"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/gtt/v1/modifyRule',
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

// cancel GTT rule
exports.cancelRule = () => {
    var data = JSON.stringify({
        "id": "5130853", 
        "symboltoken": "3045",
        "exchange": "NSE"
    });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/gtt/v1/cancelRule\n',
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

// get All GTT 
exports.getAll = () => {
    var data = JSON.stringify({
        "status": [
             "NEW",
             "CANCELLED",
             "ACTIVE",
             "SENTTOEXCHANGE",
             "FORALL"
        ],
        "page": 1,
        "count": 10
   });

    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/gtt/v1/ruleList',
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

// get Rule by id 
exports.getRuleById = () => {
    var data = JSON.stringify({ 
            "id": "5130853" 
   });
    var config = {
        method: 'post',
        url: 'https://apiconnect.angelbroking.com/rest/secure/angelbroking/gtt/v1/ruleDetails',
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
