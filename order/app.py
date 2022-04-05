from flask import Flask ,jsonify, request 
import requests

app = Flask(__name__)
orderIpAddress= "192.168.1.14"
catalogIpAddress="192.168.1.70"

@app.route('/')
def my_app():
    return 'First Flask application!'
# this req will check if there is enough books in the store and make the order

@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
    # create get req to catalog server to get the amount of book in the stock
    #then it will dec the number of books and sent aprovel; if not it will reject
    # the req
    amount = requests.get("http://"+catalogIpAddress+":5000/count/" + str(id))
    if (amount.text=="fail"):
      return jsonify({"result":"unkown Book"})
    int_amount=int(amount.text)
    
    if int_amount ==0:
         return jsonify({"result":"the stock is empty"})
    else:
     amount2=int_amount-1
     amount3=str(amount2)
     response  = requests.put("http://"+catalogIpAddress+":5000/update_amount/"+ str(id), {'amount':amount2})
    res = response.json()
    
    if (res=={'result ':"update successed"}):
      return jsonify({"result":"purchase process done successfully"})


if __name__ == '__main__':
    app.run(debug = True,port=3500),
    
    
    
    
    
    