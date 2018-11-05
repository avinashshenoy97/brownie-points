'''
Script for the peer to peer brownie network.
'''
# ==================== Imports ==================== #

from pyp2p.net import *
import json
import logging
import threading 
import time
import signal
import atexit
import argparse

import blockchain
from block import *
import transactionPool
import transaction

# ==================== Main ==================== #

class b2b: 
    msg_types = {'test', 'query_all', 'query_latest', 'response_blockchain', 'query_transaction_pool', 'response_transaction_pool'}

    def __init__(self, rendezvous_server_ip, rendezvous_server_port):
        ''' Initialises the node on the p2p network given the rendezvous server ip and port and starts the server.

            Arguments:
                rendezvous_server_ip: IP address of the rendezvous server.

                rendezvous_server_port: Port number on which the server is listening. 

        '''
        self.logger = logging.getLogger('Brownie-Network')
        self.node = Net(node_type='passive', debug=1, servers=[{'addr': rendezvous_server_ip, 'port': rendezvous_server_port}])
        self.node.start()
        self.node.bootstrap()
        self.node.advertise()
        self.exit_request = False    
        self.receiver = threading.Thread(target = self.eventLoop).start()

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        atexit.register(self.sig_handler)
    
    def sig_handler(self, signum=None, frame=None):
        ''' Signal handler for gracefully exiting after stopping all threads

            Arguments:
                signum: Indicates for which signal this handler is registered.

                frame: The stack frame.

        '''
        self.exit_request = True
        self.node.stop()
    
    def eventLoop(self):
        ''' Event loop that waits for a message from the connected peers and calls the handler when a message is recieved.

            Arguments:
                self object
            
        '''
        while not self.exit_request:
            for con in self.node:
                for reply in con:
                    self.handler(con, reply)

    def handler(self, con, msg):
        ''' Carries out the appropriate actions for the given message.

            Arguments:
                msg: JSON string message received from a peer
            
        '''
        self.logger.info('Recieved msg : ' + msg)
        msg = json.loads(msg)
        if msg['msg_type'] == 'query_latest':
            self.logger.info('Query for latest block recieved!')
            if len(blockchain.brownieChain) == 0:
                self.logger.info('Unable to respond')
                return
            msg = {'msg_type': 'response_latest', 'payload': json.dumps(blockchain.getLatestBlock(), cls=customEncoder)}
            con.send_line(json.dumps(msg))
        elif msg['msg_type'] == 'query_all':
            self.logger.info('Query for full blockchain recieved!')
            if len(blockchain.brownieChain) == 0:
                self.logger.info('Unable to respond')
                return
            msg = {'msg_type': 'response_blockchain', 'payload': json.dumps(blockchain.getBlockchain(), cls=customEncoder)}
            con.send_line(json.dumps(msg))
        elif msg['msg_type'] == 'query_transaction_pool':
            self.logger.info('Query for transaction pool recieved!')
            msg = {'msg_type': 'response_transaction_pool', 'payload': json.dumps(transactionPool.transactionPool, cls=customEncoder)}
            con.send_line(json.dumps(msg))
        elif msg['msg_type'] == 'response_latest':
            self.logger.info('Latest block received')
            newBlock = block.deserialize(json.loads(msg['payload']))
            if blockchain.isValidBlock(newBlock, blockchain.getLatestBlock()):
                blockchain.addBlockToChain(newBlock)
                self.logger.info('Added block to brownieChain')
            else:
                self.logger.error('Invalid block...')
        elif msg['msg_type'] == 'response_blockchain':
            self.logger.info('Response containing blockchain recieved!')
            recvChain = json.loads(msg['payload'])
            newChain = list()
            for b in recvChain:
                try:
                    newChain.append(block.deserialize(b))
                except Exception as e:
                    self.logger.error('An error occurred while adopting received blockchain: ' + str(e) + '\n ABORTING!')
                    return
            if len(blockchain.brownieChain) == 0:
                blockchain.genesisBrownie = newChain[0]
                blockchain.replaceChain(newChain)
                return
            if blockchain.isValidChain(newChain, blockchain.genesisBrownie):
                blockchain.replaceChain(newChain)
        elif msg['msg_type'] == 'response_transaction_pool':
            self.logger.info('Response containing transaction pool recieved!')
            newPool = list()
            for t in json.loads(msg['payload']):
                try:
                    newPool.append(transaction.Transaction.deserialize(t))
                except Exception as e:
                    self.logger.error('An error occurred while adopting received transaction pool: ' + str(e) + '\n ABORTING!')
                    return
            transactionPool.transactionPool = newPool
        elif msg['msg_type'] == 'test':
            self.logger.info('TESTING B2B!')
            print(msg)

    def validateMessage(msg):
        ''' Validates if the message that is to be sent is in the right format.

            Arguments:
                msg: The message that is to be validated.
            
            Returns:
                'True' if the message is valid and 'False' otherwise.
        '''
        if msg['msg_type'] not in b2b.msg_types:
            return False
        else:
            return True

    def broadcast(self, msg):
        ''' Broadcasts the message 'msg' to all the nodes it is currently connected to.

            Arguments:
                msg: A dictionary object containing the message that is to be sent
        '''
        if b2b.validateMessage(msg):
            self.node.broadcast(json.dumps(msg))
            self.logger.info('Broadcasting ' + str(msg))
        else:
            self.logger.error('INVALID MESSAGE : ' + msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The peer-to-peer brownie network.')
    parser.add_argument('ip', type=str)
    parser.add_argument('-p', '--port', type=int, default=8000)
    __args__ = parser.parse_args()

    obj = b2b(__args__.ip, __args__.port)
    test_msg = {'msg_type': 'test', 'payload': 'hello'}
