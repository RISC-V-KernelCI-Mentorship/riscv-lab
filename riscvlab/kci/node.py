import requests
import urllib
import logging
import argparse
from kci import BASE_URI
from config import secrets

logger = logging.getLogger(__name__)

def _get_auth_headers():
    return { "Authorization": f"Bearer {secrets.get('kci_token')}" }


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


def create_node(node_data):
    url = urllib.parse.urljoin(BASE_URI, "/node")
    logger.debug(url)
    try:
        r = requests.post(url, json=node_data, headers=_get_auth_headers())
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed at creating node: {stre(e)}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Used for testing node-related functions")
    parser.add_argument("--node-id", required=True, help="Id of the node")
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.DEBUG)

    node = get_node(args.node_id)
    print(node)

