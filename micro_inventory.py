from flask import Flask, jsonify, request
from tools import resolve_store, clean_calculation, droste_data
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)
item_details = droste_data()
current_directory = os.path.abspath(os.path.dirname(__file__))
handler = RotatingFileHandler('micro.log',
    maxBytes=1024*1024*10,
    backupCount=100
)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


@app.route('/')
def hello_world():
    return 'Micro Inventory!'


@app.route('/api/_item_lookup/<barcode>')
def api_lookup(barcode):
    app.logger.info('TESTING!')
    app.logger.warn('WARN')
    app.logger.critical('TOOTTOOT')

    try:
        barcode = barcode[:-1]
    except ValueError:
        barcode = 0

    if item_details.get(barcode.zfill(13)):
        item_detail = item_details.get(barcode.zfill(13))
        output = {
            'description': item_detail.get('description'),
            'response': 'query',
            'quantity': '0',
            'pack': '1',
            'size': '100ML',
            'upc': "{:>013}".format(barcode)
        }
    else:
        output = {
            'description': barcode,
            'response': 'query',
            'quantity': '0',
            'pack': '1',
            'size': '100ML',
            'upc': "{:>013}".format(barcode)
        }
    return jsonify(result=output)


@app.route('/api/_inventory_post/<upc>/<quantity>/<store_identifier>/<identifier>/')
def inventory_post(upc, quantity, store_identifier, identifier):

    calculation, error = clean_calculation(quantity)
    store = resolve_store(identifier)

    try:
        output = {
            'response': 'insert',
            'description': item_details[upc]["description"],
            'quantity': '{calc}'.format(calc=calculation),
            'upc': upc,
            'error': error
        }
    except AttributeError:
        output = {
            'response': 'insert',
            'description': '',
            'quantity': '0',
            'upc': '000000',
            'error': 'bad',
        }
    return jsonify(result=output)


@app.route('/api/_inventory_delete/<upc>/<quantity>/<store_identifier>/<identifier>/')
def inventory_delete(upc, quantity, store_identifier, identifier):

    calculation, error = clean_calculation(quantity)
    store = resolve_store(store_identifier)

    output = {
        'response': 'delete',
        'description': "DELETE",
        'quantity': '{calc}'.format(calc=calculation),
        'upc': upc,
        'error': error
    }

    return jsonify(result=output)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=False)
