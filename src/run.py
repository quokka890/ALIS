import maid
import journal
import config_manager
from syscommands import InstallError
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d' ,'--debug', required=False, action='store_true')
parser.add_argument('-a' ,'--advanced', required=False, action='store_true')
args = parser.parse_args()

if args.advanced:
    config_manager.generate_config(advanced_mode=True)
else:
    config_manager.generate_config()

try:
    import installer
    maid.cleanup_success()
    exit(0)
except InstallError as e:
    journal.fatal(f'Installation has failed: {e}')
    maid.cleanup_error(e)
    exit(1)