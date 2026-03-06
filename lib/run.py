from lib.maid import cleanup
import lib.installer
import atexit

atexit.register(cleanup)