from flask import Flask, jsonify
from flask_caching import Cache
import requests

URL1 = 'https://api.ratesapi.io/api/latest'
URL2 = 'https://api.exchangeratesapi.io/latest'
text = "TYPE ANOTHER CURRENCY, NO SUCH CURRENCY IN BASE"

app = Flask(__name__)

cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@app.route('/<string:id>', methods=['GET'])
def get_exrate(id):
    return jsonify(get_content(id))


@app.route('/', methods=['GET'])
def get_home():
    return "Type any Currency"


def format_url(html, name):
    if name != "latest":
        html = html + "?base=" + name
    return html


def get_content(name):
    html = format_url(URL1, name)
    response = cache.get(html)
    if response is None:
        response = requests.get(html)
        if response.status_code == 400:
            return text
        if response.status_code != 200:
            html = format_url(URL2, name)
            response = requests.get(html)
        response = response.json()
        cache.add(html, response, 60*10)
    return response


if __name__ == '__main__':
    app.run(debug=True)
