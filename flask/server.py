from flask import Flask
import xrpl
import json
import requests

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/nft', methods=['GET', 'POST'])
def mint(): 
    print('/nft is called!!')
    # data = test_mint_nft()
    data=request.form.get('data')
    app.logger.info('data')

    data_str = json.dumps(data)
    return data_str
    
if __name__ == '__main__':
   app.run()
