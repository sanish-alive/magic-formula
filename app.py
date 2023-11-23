from flask import Flask, jsonify, request
import webScraping

app = Flask(__name__)

route = {
    'open-ipo': '/open-ipo',
}

@app.route("/")
def helloFriend():
    return jsonify({'hello': 'friend'})

@app.route(route['open-ipo'])
def openIpo():
    return jsonify({'ipo': list(webScraping.openIPO())})
if __name__ == '__main__':
    app.run(debug=True)