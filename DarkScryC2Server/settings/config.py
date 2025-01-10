import configparser
import logging
import sys
import os
import queue
from logging.handlers import QueueHandler, QueueListener
from os.path import join as path_join

APP_NAME = 'DarkScryC2'
CONFIG_DIR = f'/etc/{APP_NAME}'
CONFIG_FILE = path_join(CONFIG_DIR, 'config.ini')

#
# 1. Create a logger, but don't attach normal handlers directly.
#    We will attach a QueueHandler that routes logs to a queue.
#
internalapplogger = logging.getLogger(APP_NAME)
internalapplogger.setLevel(logging.INFO)

# The shared queue for log records
log_queue = queue.Queue()

# Create a QueueHandler, which will put log records into log_queue
queue_handler = QueueHandler(log_queue)
internalapplogger.addHandler(queue_handler)

#
# 2. Create the "real" handlers that will do the actual I/O in a background thread.
#
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# We'll create a file handler for later, but we won't add it yet until we have the log path.
file_handler = None

# Now we create a QueueListener, which will pull records from the queue and pass them to the real handlers.
# We'll update it once we know the log path.
listener = None

internalapplogger.info("Starting configuration retrieval.")

def check_default_config():
    if not os.path.exists(CONFIG_DIR):
        internalapplogger.error(f"Default configuration directory {CONFIG_DIR} does not exist.")
        sys.exit(1)
    if not os.path.isfile(CONFIG_FILE):
        internalapplogger.error(f"Configuration file {CONFIG_FILE} does not exist.")
        sys.exit(1)

check_default_config()

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

log_level = config.get('logging', 'log_level', fallback='INFO').upper()
log_path = config.get('logging', 'log_path', fallback=f'/var/{APP_NAME}/app.log')

log_dir = os.path.dirname(log_path)
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
        internalapplogger.info(f"Created log directory: {log_dir}")
    except OSError as e:
        internalapplogger.error(f"Failed to create log directory {log_dir}: {e}")
        sys.exit(1)

#
# 3. Create a FileHandler with the configured log path
#
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(getattr(logging, log_level, logging.INFO))
file_handler.setFormatter(formatter)

#
# 4. Initialize the QueueListener with the "real" handlers (console + file).
#    Start it so it processes logs in a separate thread.
#
listener = QueueListener(log_queue, console_handler, file_handler, respect_handler_level=True)
listener.start()

#
# If needed, adjust the logger level now that we've loaded from config
#
internalapplogger.setLevel(getattr(logging, log_level, logging.INFO))

def check_config_section(section, keys, optional_keys=None):
    if not config.has_section(section):
        raise ValueError(f"Missing section: {section}")
    for key in keys:
        if not config.has_option(section, key) or not config.get(section, key):
            raise ValueError(f"Missing or empty {key} in section: {section}")
    if optional_keys:
        for key in optional_keys:
            if not config.has_option(section, key):
                config.set(section, key, '')

required_config = {
    'server': ['host', 'port'],
    'cryptography': ['private_key_path'],
}

optional_config = {
    'redis': ['password']
}

def is_set_up():
    all_correct = True
    for section, keys in required_config.items():
        try:
            check_config_section(section, keys)
        except ValueError as e:
            internalapplogger.error(e)
            all_correct = False
    for section, keys in optional_config.items():
        try:
            check_config_section(section, [], optional_keys=keys)
        except ValueError as e:
            internalapplogger.error(e)
            all_correct = False
    return all_correct

if not is_set_up():
    internalapplogger.error("Configuration is not set up correctly.")
    # Stop the listener before exiting
    listener.stop()
    sys.exit(1)

SERVER_HOST = config.get('server', 'host')
SERVER_PORT = int(config.get('server', 'port'))

PRIVATE_KEY_PATH = config.get('cryptography', 'private_key_path')
if not os.path.exists(PRIVATE_KEY_PATH):
    internalapplogger.error(f"{PRIVATE_KEY_PATH} does not exist.")
    listener.stop()
    sys.exit(1)

REDIS_HOST = config.get('redis', 'host', fallback='localhost')
REDIS_PORT = config.getint('redis', 'port', fallback=6379)
REDIS_DB = config.getint('redis', 'db', fallback=0)
REDIS_PASSWORD = config.get('redis', 'password', fallback=None)

REDIS_URI = f"redis://{':'+REDIS_PASSWORD if REDIS_PASSWORD else ''}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

internalapplogger.info("Configuration loaded successfully.")

# (Optional) on shutdown or right before your process ends:
# listener.stop()
