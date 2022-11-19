from flask import Flask, jsonify, request
  
app = Flask(__name__)

  
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