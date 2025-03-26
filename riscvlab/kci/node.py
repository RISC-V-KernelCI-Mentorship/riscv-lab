import requests
import urllib
import logging
import argparse
from kci import BASE_URI

logger = logging.getLogger(__name__)

def get_node(node_id):
    url = urllib.parse.urljoin(urllib.parse.urljoin(BASE_URI, "/node/"), node_id)
    logger.debug(url)
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to retrieve node: {str(e)}")
        return None
 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Used for testing node-related functions")
    parser.add_argument("--node-id", required=True, help="Id of the node")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG)

    node = get_node(args.node_id)
    print(node)

