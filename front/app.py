from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
  return "Hello World!"


# Search opearation
# return the books information( Item Number (ID),title) according to a  given topic
# this reqest send to the catalog server
@app.route('/search/<topic>', methods=['Get'])
def search(topic):
    response = requests.get("http://192.168.1.135:5000/search/" + topic)
    return response.content

# info opearation
# return  information about specific book according to given ID
# this req send to catalog server 
@app.route('/information/<int:id>', methods=['Get'])
def information_id(id):
    response = requests.get("http://192.168.1.135:5000/information/" + str(id))
    return response.content
    

if __name__ == "__main__":
  app.run(debug=True, port=3500)