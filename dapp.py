from os import environ
import os
import logging
import requests
import ipfshttpclient2
from io import BytesIO

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

data = requests.get(rollup_server + "/get_tx")
logger.info(f"Got tx {data.content}")

ipfs_api = os.getenv('IPFS_API', '/ip4/127.0.0.1/tcp/5001')

try:
    ipfs_instance = ipfshttpclient2.connect(ipfs_api)
except Exception as e:
    print(f"Error connecting to IPFS API: {e}")
    exit(1)

content = "Hello World"
directory_path = '/state'

try:
   ipfs_instance.files.mkdir(directory_path, parents=True)

   output_path = f"{directory_path}/output.file"

   ipfs_instance.files.write(output_path, BytesIO(content.encode('utf-8')), create=True, truncate=True)

except Exception as e:
    print(f"Error writing content to IPFS: {e}")



requests.post(rollup_server + "/finish", json={})
