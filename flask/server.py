from flask import Flask, jsonify, request, render_template
import xrpl
import json
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/nft', methods=['GET', 'POST'])
def mint(): 
    print('/nft is called!!')
    # data = test_mint_nft()
    response = jsonify({'Status': '200'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    if request.method == 'POST':
        print('POST request received')
        data=request.form.get('data')

        json_data = request.get_json()
        print("input data", json_data)

        file_uri = request.form["file_uri"]
        # return name + " Hello"
        print("file uri", file_uri)

        data_str = json.dumps(data)
        
        response.data = data_str
    
    return response
    
if __name__ == '__main__':
   app.run()
