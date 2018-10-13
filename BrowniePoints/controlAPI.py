'''
The HTTP API endpoints for controlling the node.
'''
# ==================== Imports ==================== #
from sanic import Sanic, Blueprint, response

import blockchain


# ==================== API ==================== #
controlAPI = Blueprint('controlAPI', url_prefix='/control')

@controlAPI.route('/getAllBlocks', methods=['GET'])
async def getAllBlocks(request):
    return response.json(blockchain.brownieChain)


@controlAPI.route('/mineBlock', methods=['POST'])
async def mineBlock(request):
    return response.json(blockchain.generateNextBlock(request.json['data']))

@controlAPI.route('/getAllPeers', methods=['GET'])
async def getAllPeers(request):
    return response.json(blockchain.browniePeers)

@controlAPI.route('/addPeer/<peer>')
async def addPeer(request, peer):
    blockchain.connectToPeer(peer)
    return response.json({}, status=200)