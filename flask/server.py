from flask import Flask, jsonify, request, render_template
import xrpl
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "http://127.0.0.1"}})
app.debug = True


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/nft', methods=['GET', 'POST'])
def mint(): 
    print('/nft is called!!')
    # data = test_mint_nft()
    response = jsonify({'Status': '200'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Access-Control-Allow-Domain'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    
    if request.method == 'POST':
        json_data = request.get_json()
        print("input data", json_data)
        print("input data type: ", type(json_data))

        print('POST request received')
        data=request.json.get('file_url')
        print("atttempt zero: file uri", data)

        print('POST request received')
        data=request.form.get('file_url')
        print("atttempt one: file uri", data)

        file_uri = request.form["file_url"]
        # return name + " Hello"
        print("attempt two file uri", file_uri)

        file_uri = request.json['file_uri']
        print("attempt three: file uri", file_uri)

        




        data_str = json.dumps(data)
        
        response.data = data_str
    
    return response
    
if __name__ == '__main__':
   app.run()
