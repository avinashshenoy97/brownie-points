import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# main_dir = os.path.dirname(parentdir)
sys.path.insert(0,currentdir)

__all__ = []
__version__ = '0.0.1'
