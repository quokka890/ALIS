from halo import Halo
import logging
import maid
logging.basicConfig(filename="logs.txt", level=logging.INFO)

journal = Halo(text="text", spinner='dots')

def info(text):
    journal.info(text=text)
    logging.info(f'{text}')

def warn(text):
    journal.warn(text=text)
    logging.warn(f'{text}')

def success(text):
    journal.succeed(text=text)
    logging.info(f'{text}')

def load(text):
    journal(text=text, spinner='dots')

def log_command(text):
    logging.info(f'{text}')

def log_command_err(text):
    logging.critical(f'{text}')

def fatal(text):
    journal.warn(text = text)
    logging.critical(f'{text}')
    maid.cleanup(Called_By_AtExit=False, ExitCode=1)