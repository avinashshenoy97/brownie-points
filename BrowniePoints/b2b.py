'''
Script for the peer to peer brownie network.
'''
# ==================== Imports ==================== #

from pyp2p.net import *
#from blockchain import *
import json
import logging
import threading 
import time
import signal

# ==================== Main ==================== #

class b2b: 
    def __init__(self, rendezvous_server_ip='52.14.188.36', rendezvous_server_port=8000):
        ''' Initialises the node on the p2p network given the rendezvous server ip and port and starts the server.

            Arguments:
                rendezvous_server_ip: IP address of the rendezvous server.

                rendezvous_server_port: Port number on which the server is listening. 

        '''
        self.node = Net(node_type="passive", debug=1, servers=[{"addr": rendezvous_server_ip, "port": rendezvous_server_port}])
        self.node.start()
        self.node.bootstrap()
        self.node.advertise()
        self.logger = logging.getLogger('Brownie-Network')
        self.exit_request = False    
        self.receiver = threading.Thread(target = self.eventLoop).start()

        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
    
    def sig_handler(self, signum, frame):
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
                    self.handler(reply)

    def handler(self, msg):
        ''' Carries out the appropriate actions for the given message.

            Arguments:
                msg: JSON string message received from a peer
            
        '''
        self.logger.info("Recieved msg : " + msg)
        print(msg)

    def validateMessage(msg):
        ''' Validates if the message that is to be sent is in the right format.

            Arguments:
                msg: The message that is to be validated.
            
            Returns:
                'True' if the message is valid and 'False' otherwise.
        '''
        msg_types = ['query_all', 'query_latest', 'response_blockchain']
        
        if msg['msg_type'] not in msg_types:
            return False
        else:
            return True

    def broadcast(self, msg):
        ''' Broadcasts the message 'msg' to all the nodes it is currently connected to.

            Arguments:
                msg: A dictionary object containing the message that is to be sent
        '''
        global logger

        if validateMessage(msg):
            self.node.broadcast(json.dumps(msg))
        else:
            self.logger.error('Message : ' + msg + ' is invalid')


if __name__ == '__main__':
    obj = b2b()
    test_msg = {"msg_type": "query_all", "payload": "hello"}
