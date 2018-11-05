'''
Main script for Brownie Points.
'''
# ==================== Imports ==================== #
import logging
import os
from datetime import datetime as dt
import argparse
from sanic import Sanic, response
import subprocess as sp
import sys
import atexit
import time

from block import block
import blockchain
import transactionPool
import wallet
from b2b import b2b
from controlAPI import controlAPI


# ==================== Command Line Arguements ==================== #
parser = argparse.ArgumentParser(description='Brownie Points - New Age, Quantum Resistant CryptoCurrency and ex-social currency.')

parser.add_argument('-d', '--debug', default=False, action='store_true', help='Run in debug mode.')
parser.add_argument('-f', '--first', default=False, action='store_true', help='First node, automatically starts rendezvous server.')
parser.add_argument('-w', '--wallet', default=False, action='store_true', help='Create new keypair for wallet.')
parser.add_argument('-m', '--miner', default=False, action='store_true', help='Start as a client that mines continuously.')
parser.add_argument('-na', '--no-api', default=False, action='store_true', help='Don\'t start the REST API.')
parser.add_argument('rendezvous_ip', type=str, help='Rendezvous server IP address.')
parser.add_argument('rendezvous_port', type=str, default=8000, help='Rendezvous server PORT at IP address.')
parser.add_argument('-p', '--port', type=int, default=16000, help='REST API port to listen on.')

__args__ = parser.parse_args()
if __args__.debug:
    print(__args__)


# ==================== Config and Globals ==================== #
atexit.register(lambda: logging.shutdown())

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

if __args__.debug:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.DEBUG, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    print(logging.getLogger().handlers)
else:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.INFO, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')

logging.getLogger('pyp2p').setLevel(logging.INFO)
brownieLogger = logging.getLogger('MainBrownie')

app = Sanic('BrowniePoints')

app.blueprint(controlAPI)

@app.route('/favicon.ico', methods=['GET',])
def favicon_handler(request):
    return response.json({}, status=404)


if __args__.first:
    sp.Popen(['python3', 'BrowniePoints/rendezvous-server/rendezvous_server.py'])
    brownieLogger.debug(str(blockchain.brownieChain))
    time.sleep(2)
    brownieLogger.info('Joining b2b network')
    brownieNet = b2b(__args__.rendezvous_ip, __args__.rendezvous_port)
    blockchain.brownieNet = brownieNet
    transactionPool.brownieNet = brownieNet
    brownieLogger.info('Mmmmm... that fresh brownie smell in the air!')
    blockchain.init()
    brownieLogger.info('Created genesis brownie and initiated own blockchain.')
else:
    brownieLogger.info('Joining b2b network')
    brownieNet = b2b(__args__.rendezvous_ip, __args__.rendezvous_port)
    blockchain.brownieNet = brownieNet
    transactionPool.brownieNet = brownieNet
    brownieLogger.info('Synchronizing with brownie network!')
    brownieNet.broadcast({'msg_type': 'query_all'})
    brownieLogger.debug(str(blockchain.brownieChain))


brownieLogger.info('Initialising wallet...')
if __args__.wallet:
    os.system('rm -rf Wallet')
wallet.initWallet()

if not __args__.no_api:
    brownieLogger.info('Starting brownie API')
    if __args__.debug:
        app.run(host='0.0.0.0', port=__args__.port, debug=True, access_log=True)
    else:
        app.run(host='0.0.0.0', port=__args__.port, debug=False, access_log=True)