import json
import requests
import logging
from libs.requests import create_session
from libs.jwt import generate_jwt

logger = logging.getLogger(__name__)

def github_post(url, payload, token):
    headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }
    s = create_session("https://api.github.com")
    try:
        r = s.post(url,
               data=json.dumps(payload).encode(),
               headers=headers)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not post send request: {str(e)}") 
        raise RuntimeError(str(e))


def github_get(url, token):
    headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
    }
    s = create_session("https://api.github.com")
    try:
        r = s.get(url,
               headers=headers)
        r.raise_for_status()
        return r
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not get send request: {str(e)}")
        raise RuntimeError(str(e))


def get_installation_token(pem_file, client_id, owner, repo):
    jwt_token = generate_jwt(pem_file, client_id)
    r_install = github_get(f"https://api.github.com/repos/{owner}/{repo}/installation", jwt_token)
    installation = r_install.json()
    install_id = installation["id"]
    payload = {
            "repositories":[repo],
            "permissions":{"actions":"write"}
    }
    r_token = github_post(f"https://api.github.com/app/installations/{install_id}/access_tokens",
                          payload, jwt_token)
    token = r_token.json()
    return token["token"]

