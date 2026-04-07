from halo import Halo
import logging
import sys
import inspect
# clear log file on each run
open("logs.txt", "w").close()

logging.basicConfig(
    filename="logs.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger()

spinner = Halo(spinner="dots")
_current_section = None

def section(title, omit = False):
    global _current_section
    if title == _current_section:
        return
    _current_section = title

    if spinner.enabled and omit == False:
        spinner.stop()

    separator = "=" * 40
    log.info(f"\n{separator}\n  {title}\n{separator}")
    if omit == False:
        spinner.text = title
        spinner.start()

def info(msg, omit = False):
    log.info(msg)
    if omit == False:
        spinner.info(msg)

def warn(msg, omit = False):
    log.warning(msg)
    if omit == False:
        spinner.warn(msg)
        spinner.start()

def success(msg="Success"):
    log.info(f"SUCCESS: {msg}")
    spinner.succeed(f'{_current_section} - {msg}')

def debug(msg):
    log.debug(f'DEBUG: {msg}')
    spinner.warn(f'DEBUG: {msg}')

def fatal(msg):
    log.fatal(msg)
    spinner.fail(msg)

def log_command(msg):
    log.info(msg)