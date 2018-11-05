'''
The HTTP API endpoints for controlling the node.
'''
# ==================== Imports ==================== #
import logging
from sanic import Sanic, Blueprint, response
from sanic.exceptions import ServerError

import blockchain
import transactionPool
import wallet


# ==================== API ==================== #
logger = logging.getLogger('APILogger')
controlAPI = Blueprint('controlAPI', url_prefix='/control')


@controlAPI.route('/getAllBlocks', methods=['GET'])
async def getAllBlocks(request):
    return response.json(blockchain.brownieChain)


@controlAPI.route('/getTransactionPool', methods=['GET'])
async def getAllBlocks(request):
    return response.json(transactionPool.getTransactionPool())


@controlAPI.route('/getUnspentTxOuts', methods=['GET'])
async def getUnspentTxOuts(request):
    return response.json(blockchain.unspentTxOuts)


@controlAPI.route('/mineRawBlock', methods=['POST'])
async def mineRawBlock(request):
    return response.json(blockchain.generateRawNextBlock(request.json['data']))


@controlAPI.route('/mineBlock', methods=['PUT'])
async def mineBlock(request):
    return response.json(blockchain.generateNextBlock())


@controlAPI.route('/getWalletAddress', methods=['GET'])
async def getWalletAddress(request):
    return response.json({'address': wallet.getPublicFromWallet()})


@controlAPI.route('/sendTransaction', methods=['POST'])
async def sendTransaction(request):
    if not 'address' in request.json:
        raise ServerError('`address` is required!', status=400)
    if not 'amount' in request.json:
        raise ServerError('`amount` is required!', status=400)

    logger.info('Sending ' + str(request.json['amount']) + ' to ' + str(request.json['address']))
    return response.json(wallet.sendTransaction(request.json['address'], float(request.json['amount'])))

