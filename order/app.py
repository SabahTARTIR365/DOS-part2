from flask import Flask ,jsonify, request 
#import requests

app = Flask(__name__)
orderIpAddress= "192.168.1.14"
catalogIpAddress="192.168.1.13"
# this req will check if there is enough books in the store and make the order
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
    # create get req to catalog server to get the amount of book in the stock
    #then it will dec the number of books and sent aprovel; if not it will reject
    # the req
    amount = requests.get("http://"+catalogIpAddress+":5000/count/" + str(id))
    if amount ==0:
         return jsonify({"result":"the stock is empty"})
    else:
     response  = requests.put("http://"+catalogIpAddress+"5000/update/"+ str(id), {'amount':amount-1})
     x = response.json()

     if x['result'][0] =="decreased quantity sucsesfully":
        return "the order was placed"
     else :  return "the order was cancelled"

if __name__ == '__main__':
    app.run(debug = True,port=3500),

