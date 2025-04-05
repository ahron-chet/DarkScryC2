import logging
import sys
import os
import queue
from logging.handlers import QueueHandler, QueueListener
# from dotenv import load_dotenv

APP_NAME = 'DarkScryC2Server'
ENV_FILE = "/env/c2server.env" #os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))

# Load .env file
# if not os.path.isfile(ENV_FILE):
#     print(f"Environment file {ENV_FILE} does not exist.")
#     sys.exit(1)

# load_dotenv(ENV_FILE)

# Logger setup
internalapplogger = logging.getLogger(APP_NAME)
log_queue = queue.Queue()
queue_handler = QueueHandler(log_queue)
internalapplogger.addHandler(queue_handler)

# Real handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Retrieve logging configs
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
log_path = os.getenv('LOG_PATH', f'/var/{APP_NAME}/app.log')

# Ensure log directory exists
log_dir = os.path.dirname(log_path)
os.makedirs(log_dir, exist_ok=True)

file_handler = logging.FileHandler(log_path)
file_handler.setLevel(getattr(logging, log_level, logging.INFO))
file_handler.setFormatter(formatter)

# QueueListener setup
listener = QueueListener(log_queue, console_handler, file_handler, respect_handler_level=True)
listener.start()
internalapplogger.setLevel(getattr(logging, log_level, logging.INFO))

# Required environment variables
required_env_vars = ['C2_SERVER_HOST', 'C2_SERVER_PORT']

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    internalapplogger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    # listener.stop()
    # sys.exit(1)

SERVER_HOST = os.getenv('C2_SERVER_HOST')
SERVER_PORT = int(os.getenv('C2_SERVER_PORT'))

PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')
if PRIVATE_KEY_PATH and not os.path.exists(PRIVATE_KEY_PATH):
    internalapplogger.error(f"Private key file {PRIVATE_KEY_PATH} does not exist.")
    # listener.stop()
    # sys.exit(1)

# Redis config
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
REDIS_DB = int(os.getenv('C2_SERVER_REDIS_DB', '0'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS_URI = f"redis://{':' + REDIS_PASSWORD if REDIS_PASSWORD else ''}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

internalapplogger.info("Configuration loaded successfully.")

