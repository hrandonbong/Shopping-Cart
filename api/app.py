from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

@app.route("prices", methods=["POST"])
def prices():
    if request.form:
        input = request.form
    elif request.json:
        input = request.json
    item = input["item"]
    url = "https://www.google.com/search?q=" + item + "&tbm=shop"
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    price = soup.find("span",{"class":"HRLxBb"})
    return price.text, 200,{'Content-Type': 'text/plain'}

if __name__== '__main__':
    app.run(debug=True)