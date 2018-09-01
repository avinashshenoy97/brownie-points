'''
Main script for Brownie Points.
'''
# ==================== Imports ==================== #
import logging
from datetime import datetime as dt
import argparse

from block import block


# ==================== Command Line Arguements ==================== #
parser = argparse.ArgumentParser(description='Brownie Points - New Age, Quantum Resistant CryptoCurrency and ex-social currency.')

parser.add_argument('--debug', default=False, action='store_true')

__args__ = parser.parse_args()


# ==================== Config and Globals ==================== #
if __args__.debug:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.DEBUG, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')
else:
    logging.basicConfig(filename='BrowniePoints.log', level=logging.INFO, format='%(asctime)-15s - %(name)s - %(levelname)s -- %(message)s')

brownieLogger = logging.getLogger('MainBrownie')

genesisBlock = block(0, '7bbf374f987ffc593c6e28a4d558c3a299a9346e98c6448ef4c0c8d248078a36', None, dt.now(), 'the holy brownie')
blockchain = [genesisBlock]

