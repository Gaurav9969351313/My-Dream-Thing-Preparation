from flask import Flask, jsonify, request
  
app = Flask(__name__)

def getHeader():
    # Accept:application/json
    # x-user-info:USER##{{UserID}}##0##{{SessionID}}
    # X-PrivateKey:smartapi_key
    # Authorization:Bearer {{jwtToken}}
    # X-SourceID:WEB
    # X-ClientLocalIP:172.29.24.173
    # X-ClientPublicIP:172.29.24.173
    # X-MACAddress:e0:d5:5e:91:23:d4
    # X-UserType:USER
  
@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})
  
  
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
        return jsonify({'data': num**2})


@app.route('/getOrderBook', methods = ['GET'])
def getOrderBook():
    try:
        return jsonify({'data': 2**2})
    except:
        pass

  
if __name__ == '__main__':
    app.run(debug = True)