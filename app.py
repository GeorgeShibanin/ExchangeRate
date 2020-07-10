from flask import Flask, jsonify, make_response
import requests
from functools import lru_cache

URL = 'https://api.ratesapi.io/api/latest'
text = "TYPE ANOTHER CURRENCY, NO SUCH CURRENCY IN BASE"

app = Flask(__name__)


@app.route('/<string:id>', methods=['GET'])
def get_exrate(id):
    return get_content(URL, id)


def format_data(text):
    text = text.replace("\"", "")
    return text


@lru_cache(maxsize=128)
def get_content(html, name):
    if name != "latest":
        html = html + "?base=" + name
    response = requests.get(html).text
    if response == "{\"error\":\"Base \'"+name+"\' is not supported.\"}":
        return text
    return format_data(response)


if __name__ == '__main__':
    app.run(debug=True)
