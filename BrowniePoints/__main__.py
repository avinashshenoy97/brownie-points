'''
Main script for Brownie Points.
'''
# ==================== Imports ==================== #
import logging
from datetime import datetime as dt
import argparse
from sanic import Sanic, response
import subprocess as sp
import sys
import atexit

from block import block
import blockchain
from b2b import b2b
from controlAPI import controlAPI

# ==================== Command Line Arguements ==================== #
parser = argparse.ArgumentParser(description='Brownie Points - New Age, Quantum Resistant CryptoCurrency and ex-social currency.')

parser.add_argument('--debug', default=False, action='store_true')
parser.add_argument('--first', default=False, action='store_true')
parser.add_argument('--no-api', default=False, action='store_true')
parser.add_argument('rendezvous_ip', type=str)
parser.add_argument('rendezvous_port', type=str, default=8000)
parser.add_argument('--p', '--port', type=int, default=16000)

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

blockchain.init()
brownieLogger.info('Created genesis brownie and initiated own blockchain.')

app = Sanic('BrowniePoints')

app.blueprint(controlAPI)

@app.route('/favicon.ico', methods=['GET',])
def favicon_handler(request):
    return response.json({}, status=404)


if __args__.first:
    sp.Popen(['python3', 'BrowniePoints/rendezvous-server/rendezvous_server.py'])
    print('TEST')
    brownieLogger.info('Mmmmm... that fresh brownie smell in the air!')
    blockchain.brownieChain.append(blockchain.generateNextBlock('test'))
    brownieLogger.debug(str(blockchain.brownieChain))
    brownieLogger.info('Joining b2b network')
    brownieNet = b2b(__args__.rendezvous_ip, __args__.rendezvous_port)
else:
    brownieLogger.info('Joining b2b network')
    brownieNet = b2b(__args__.rendezvous_ip, __args__.rendezvous_port)
    brownieLogger.info('Synchronizing with brownie network!')
    brownieNet.broadcast({'msg_type': 'query_all'})
    brownieLogger.debug(str(blockchain.brownieChain))

blockchain.brownieNet = brownieNet

if not __args__.no_api:
    brownieLogger.info('Starting brownie API')
    if __args__.debug:
        app.run(host='0.0.0.0', port=__args__.port, debug=True, access_log=True)
    else:
        app.run(host='0.0.0.0', port=__args__.port, debug=False, access_log=True)