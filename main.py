from flask import Flask,  render_template, request
from datetime import date
import requests
from models import Pair, ConvertedPair
import config

app = Flask(__name__)
base_url = 'https://api.getgeoapi.com/v2/currency/'
params = {'api_key': config.api_key , 'format': 'json'}

@app.route('/', methods=['GET','POST'])
def index():

    response_conversion = []
    for_currency = ''
    if request.method == 'POST':
        amount = request.form.get('amount')
        base_currency = request.form.get('baseCurrency')
        for_currency = request.form.get('toCurrency')

        params_convert = {'api_key': config.api_key, 
                            'format': 'json',
                            'from': base_currency,
                            'to': for_currency,
                            'amount': amount}

        response_conversion = requests.get(base_url + 'convert', params_convert).json()

    today_date = date.today().strftime('%Y-%m-%d')
    main_pairs = ['USD', 'GBP', 'JPY', 'CHF', 'CAD']
    main_pairs_conversions = []
    all_pairs = []

    response = requests.get(base_url + 'list', params).json()
    for key,value in response['currencies'].items():
        all_pairs.append(Pair(key, value))
    
    pairs_conversions = []
    for pair in main_pairs:
        params['from'] = 'EUR'
        params['to'] = pair
        response = requests.get(base_url + f'historical/{today_date}', params).json()
        main_pairs_conversions.append(ConvertedPair(params["from"], params["to"], response["rates"][pair]["rate"]))
    
    return render_template("index.html", conversions = main_pairs_conversions
                                       , pairs = all_pairs
                                       , conversion = response_conversion
                                       , for_currency = for_currency)

if __name__ == '__main__':
    app.run(debug=True)