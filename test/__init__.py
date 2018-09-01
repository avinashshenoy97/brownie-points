'''
Set the context for tests to import the libraries from the right directories.
'''
# =============== Imports =============== #
import os, sys
import logging


# =============== Context =============== #
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/brownie-points')