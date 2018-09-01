'''
Main script for Brownie Points.
'''
# ==================== Imports ==================== #
import logging
from datetime import datetime as dt
import argparse
from sanic import Sanic
from sanic import response

from block import block
import blockchain
from controlAPI import controlAPI


# ==================== Command Line Arguements ==================== #
parser = argparse.ArgumentParser(description='Brownie Points - New Age, Quantum Resistant CryptoCurrency and ex-social currency.')

parser.add_argument('--debug', default=False, action='store_true')
parser.add_argument('-p', '--port', type=int, default=16000)

__args__ = parser.parse_args()


# ==================== Config and Globals ==================== #
if __args__.debug:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.DEBUG, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')
else:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.INFO, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')

brownieLogger = logging.getLogger('MainBrownie')

blockchain.init()
brownieLogger.info('Created genesis brownie and initiated own blockchain.')

app = Sanic('BrowniePoints')

app.blueprint(controlAPI)

@app.route('/favicon.ico', methods=['GET',])
def favicon_handler(request):
    return response.json({}, status=404)


if __args__.debug:
    app.run(host='0.0.0.0', port=__args__.port, debug=True, access_log=True)
else:
    app.run(host='0.0.0.0', port=__args__.port, debug=False, access_log=True)