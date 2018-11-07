'''
Unit tests for BrowniePoints

Run tests using : nosetests -v UnitTests/
'''
import sys
import os
import subprocess as sp
from time import sleep

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../BrowniePoints')))

import blockchain

brownieNet = None
rendezvousServer = None

def setup_package():
    
    ''' Package level setup function
    '''

    global brownieNet
    global rendezvousServer

    if rendezvousServer is None :
        rendezvousServer = sp.Popen(['python3', '../BrowniePoints/rendezvous-server/rendezvous_server.py'], stderr=open('/dev/null'), stdout=open('/dev/null'))
        sleep(2)

    if brownieNet is None :
        brownieNet = blockchain.b2b('127.0.0.1', 8000)
        blockchain.brownieNet = brownieNet

        
def teardown_package():
    
    ''' Package level teardown function
    '''

    global brownieNet
    global rendezvousServer

    if brownieNet is not None :
        brownieNet.sig_handler()
    if rendezvousServer is not None :
        rendezvousServer.kill()
