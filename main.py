from flask import Flask, render_template, jsonify, request
import spacy
import requests

nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/submit')
def submit():
    email = request.args.get("email")
    content = request.args.get("content")

    # here is the machine learning piece


    doc = nlp(content)

    keys = ['buy', 'sell', 'long', 'short' , 'hedge']
    intend = None

    for token in doc:
        if (token.text.lower() in keys):
            intend = token.text

    if intend == 'buy':
        intend = 'long'
    if intend == 'sell':
        intend = 'short'

    count = 0
    dic_list = []

    for entity in doc.ents:
        if (entity.label_ == 'ORG'):
            count = count + 1
            dic_list.append({'TYPE': intend})


    for entity in doc.ents:
        for d in dic_list:
            if entity.label_ not in d.keys():
                if entity.label_ == 'ORG':

                    companyName = entity.text

                    url = 'https://services.dowjones.com/autocomplete/data?q='
                    webUrl = url + companyName

                    r = requests.get(webUrl)
                    contents = r.json()
                    ticker = ''

                    if len(contents.get("symbols")) > 0:
                        ticker = contents.get("symbols")[0].get("ticker")
                        print (ticker);
                        d[entity.label_] = ticker # Need ticker lookup
                        price_url = 'https://api.iextrading.com/1.0/stock/' + ticker + '/chart';
                        getPrice = requests.get(price_url).json();
                        stockPrice = getPrice[len(getPrice)-1].get("close");
                        d["market_price"] = stockPrice
                    else:
                        d[entity.label_] = ''
                        d["market_price"] = ''
                else:
                    d[entity.label_] = entity.text
                    if "market_price" not in d.keys():
                        d["market_price"] = ''
                break


    for d in dic_list:
        if "MONEY" not in d.keys():
            d["METHOD"] = 'market price'
            d["MONEY"] = '-'
        else:
            d["METHOD"] = 'fix price'

    return jsonify({
            "email": email,
            "order":dic_list  # execute method: market price or fix price
    })

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=10001, debug=True)
