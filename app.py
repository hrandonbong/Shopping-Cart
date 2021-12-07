from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
cart = {}
currID = 1

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

@app.route("/")
def index():
    return render_template("index.html")

#--------- HTTP REQUEST ----------#
@app.route("/add",methods=["GET","POST"])
def append():
    global currID
    if request.method == "POST":
        output = request.form.get("items")
    else:
        output = request.args.get("items")

        url1 = 'https://zacharylevatoncs361.herokuapp.com/images'
        url2 = 'https://cs361shoppingcart.herokuapp.com/prices'
        myobj1 = {'keyword':output}
        image = requests.post(url1,data=myobj1).text
        link = "https://www.ralphs.com/search?query=" + output
        myobj2 = {'items':output}
        price = requests.post(url2,data=myobj2).text

    cart[currID] = [output, image, link, price]
    currID += 1
    return render_template("index.html",items=cart)

def apiLinks(item):
        # input = request.json
        # item = input["item"]
        url = "https://www.google.com/search?q=" + item + "&tbm=shop"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        price = soup.find("span", {"class": "HRLxBb"})
        return price.text

@app.route("/complete/<id>")
def delete(id):
    del cart[int(id)]
    if len(cart) == 0:
        return render_template("index.html")
    else:
        return render_template("index.html",items=cart)


if __name__== '__main__':
    app.run()