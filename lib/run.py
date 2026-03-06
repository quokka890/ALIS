from lib.maid import cleanup
import atexit
import lib.installer


atexit.register(cleanup)