from flask import Flask
from flask import request
import requests
app = Flask(__name__)
orderIpAddress1= "192.168.1.14"
orderIpAddress2= "192.168.1.15"
catalogIpAddress1="192.168.1.70"
catalogIpAddress2="192.168.1.71"

catalog_counter = 1 
order_counter = 1 
def catalog_round_robin():
    global catalog_counter
    #round robin between catalog servers 
    if(catalog_counter ==1):
      catalogIpAddress=catalogIpAddress1
      catalog_counter = 2
    if(catalog_counter ==2):
      catalogIpAddress=catalogIpAddress2
      catalog_counter = 1
    return  catalogIpAddress

def order_round_robin():
    global order_counter
    #round robin between catalog servers 
    if(order_counter ==1):
      orderIpAddress=orderIpAddress1
      order_counter = 2
    if(order_counter ==2):
      orderIpAddress=orderIpAddress2
      order_counter = 1  
    return  orderIpAddress
     
@app.route("/")
def hello():
  return "Hello World!"


# Search opearation
# return the books information( Item Number (ID),title) according to a  given topic
# this reqest send to the catalog server
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
    catalogIpAddress=catalog_round_robin()
    response = requests.get("http://"+catalogIpAddress+":5000/search/" + topic)
    return response.content

# info opearation
# return  information about specific book according to given ID
# this req send to catalog server 
@app.route('/info/<int:id>', methods=['Get'])
def information_id(id):
    response = requests.get("http://"+catalogIpAddress+":5000/info/" + str(id))
    return response.content

# purchase opearation
#this post req will be sent to ORDER server in order to purchase specific book
@app.route('/purchase/<int:id>', methods=['Post'])
def purchase(id):
    orderIpAddress=order_round_robin()
    response = requests.post("http://"+orderIpAddress+":5000/purchase/" + str(id))
    return response.content

# this req will be used from the internal system by the admin in order to
#update price of specific book - it will send to catalog server
@app.route('/update_price/<int:id>', methods=['Put'])
def update_price(id):
    catalogIpAddress=catalog_round_robin()
    price = request.json['price']
    response = requests.put("http://"+catalogIpAddress+":5000/update_price/" + str(id), {'price': price})
    return response.content

if __name__ == "__main__":
  app.run(debug=True, port=3500)