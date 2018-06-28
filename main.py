from flask import Flask, render_template, jsonify, request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/submit')
def submit():
    email = request.args.get("email")
    content = request.args.get("content")

    # here is the machine learning piece

    return jsonify({
            "typeOfForm": "",  # booking or request pricing
            "ticker": "",  # ticker or company name
            "shares": "",  # quantity
            "price": "",    # price
            "method": ""    # execute method: market price or fix price
    })

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=10001, debug=True)
