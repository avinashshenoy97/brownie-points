import asyncio
import websockets as ws
from enum import Enum
import json
from blockchain import addBlockToChain, Block, getBlockchain, getLatestBlock, handleReceivedTransaction, isValidBlockStructure,replaceChain
from transaction import Transaction
from transactionPool import getTransactionPool
sockets=[]

class MessageType(Enum):
	QUERY_LATEST = 0
	QUERY_ALL = 1
	RESPONSE_BLOCKCHAIN = 2
	QUERY_TRANSACTION_POOL = 3
    RESPONSE_TRANSACTION_POOL = 4
	
'''
Not sure if this should be written
 public type: MessageType;
  public data: any;

'''
class Message:
	

	
def initP2PServer(p2pPort):	
	server = websockets.serve(initConnection, 'localhost', p2pPort)
	'''On the server side, websockets executes the handler coroutine hello once for each WebSocket connection. It closes the connection when the handler coroutine returns'''
	'''server.on('connection', (ws: WebSocket) => {
        
    });'''
	#initConnection(ws)
    logger.error('listening websocket p2p port on: ' + p2pPort);

#const getSockets = () => sockets;   --- Idk
def initConnection(ws):
	#sockets.push(ws)
	await websocket.send(ws)
	initMessageHandler(ws)
    initErrorHandler(ws)
    print(ws, queryChainLengthMsg())

r = Timer(500, broadcast(), (queryTransactionPoolMsg()))	
r.start()

	
def JSONToObject(data):
	try:
		return JSON.parse(data)
  
	except:
	{
		logger.error(e);
        return null;
    }
	
def initMessageHandler(ws):	
	name = await websocket.recv()
	'''
	try {
            const message: Message = JSONToObject<Message>(data);
            if (message === null) {
                console.log('could not parse received JSON message: ' + data);
                return;
            }
            console.log('Received message: %s', JSON.stringify(message));
	
	'''
	try:
		message=JSONToObject(data)
		if (message === null):
			logger.error('could not parse received JSON message: ' + data)
			return;
        logger.error('Received message: %s', JSON.stringify(message));
	
		switch (message.type):
			case MessageType.QUERY_LATEST:
				write(ws, responseLatestMsg())
				break;
			case MessageType.QUERY_ALL:
				write(ws, responseChainMsg())
				break;
			case MessageType.RESPONSE_BLOCKCHAIN:
				receivedBlocks = JSONToObject(message.data)
				if (receivedBlocks == null):
					logger.error('invalid blocks received: %s', JSON.stringify(message.data))
					break
				handleBlockchainResponse(receivedBlocks)
				break
			case MessageType.QUERY_TRANSACTION_POOL:
				write(ws, responseTransactionPoolMsg())
				break
			case MessageType.RESPONSE_TRANSACTION_POOL:
				receivedTransactions = JSONToObject(message.data)
				if (receivedTransactions == null):
					logger.error('invalid transaction received: %s', JSON.stringify(message.data))
					break
			#receivedTransactions.forEach((transaction: Transaction):  --->
				try:
					handleReceivedTransaction(transaction)
					broadCastTransactionPool()
				except:
					logger.error(e.message)
			break
	except:
		logger.error(e)
                    
	
	
def write(ws,message):
	#await websocket.send(name)	
	#json.dumps(message)
	await websocket.send(json.loads(json.dumps(message)))

#const broadcast = (message: Message): void => sockets.forEach((socket) => write(socket, message));
#---const getSockets = () => sockets;  --- figure out this function
def broadcast(message):
	forEach(socket in sockets):
		write(socket,message)
		
def queryChainLengthMsg():
	'type': MessageType.QUERY_LATEST
	'data': null
	
def queryAllMsg():
	'type': MessageType.QUERY_ALL
	'data': null

def responseChainMsg():
	'type': MessageType.RESPONSE_BLOCKCHAIN	
	'data': json.loads(json.dumps(getBlockchain()))

def responseLatestMsg():
	'type': MessageType.RESPONSE_BLOCKCHAIN	
	'data':json.loads(json.dumps([getLatestBlock()]))

def queryTransactionPoolMsg():
	'type': MessageType.QUERY_TRANSACTION_POOL
    'data': null	
	
def responseTransactionPoolMsg():
	'type': MessageType.RESPONSE_TRANSACTION_POOL
    'data': json.loads(json.dumps(getTransactionPool()))

def splice(index,num_eles):
	'''
	splice() method changes the content of an array, adding new elements while removing old elements.
	If you don't specify any elements, splice simply removes the elements from the array
	Eg:
	var array=[1,2,3,4,5];
console.log(array.splice(2));
// shows [3, 4, 5], returned removed item(s) as a new array object.
	'''
		
def initErrorHandler(ws):
	def closeConnection(myWs):
		logger.error('connection failed to peer: ' + myWs.url)
		sockets.splice(sockets.indexOf(myWs), 1);



def handleBlockchainResponse(receivedBlocks):
	if (receivedBlocks.length ==0):
		logger.error('received block chain size of 0')
        return;
	latestBlockReceived=receivedBlocks[receivedBlocks.length - 1]
	if (!isValidBlockStructure(latestBlockReceived)):
		logger.error('block structuture not valid');
        return;
	latestBlockHeld	= getLatestBlock()
	if (latestBlockReceived.index > latestBlockHeld.index):
		logger.error('blockchain possibly behind. We got: '
            + latestBlockHeld.index + ' Peer got: ' + latestBlockReceived.index)
		if (latestBlockHeld.hash == latestBlockReceived.previousHash):	
			if (addBlockToChain(latestBlockReceived)):
				broadcast(responseLatestMsg())
		else if (receivedBlocks.length === 1):
            logger.error('We have to query the chain from our peer')
            broadcast(queryAllMsg());
		else:
            logger.error('Received blockchain is longer than current blockchain')
            replaceChain(receivedBlocks)
	else:
		logger.error('received blockchain is not longer than received blockchain. Do nothing')
		

def broadcastLatest():
	broadcast(responseLatestMsg())
        		
def connectToPeers(newPeer):				
	#Not sure
	
def broadCastTransactionPool():	
	broadcast(responseTransactionPoolMsg())