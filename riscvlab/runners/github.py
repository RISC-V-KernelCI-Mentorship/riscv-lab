import json
import requests
import logging
import argparse
from libs.requests import create_session
from libs.jwt import generate_jwt
from libs.github import github_post, get_installation_token
from config import secrets

logger = logging.getLogger(__name__)

class GitHubRunner:

    def __init__(self, secrets_key, owner, repo, workflow_id, client_id_key):
        self.__github_url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches"
        self.__secrets_key = secrets_key
        self.__client_id_key = client_id_key
        self.__owner = owner
        self.__repo = repo

    def __call__(self, kernel_url, selftests_url, modules_url, build_id):
        logger.debug("Running GitHub action")
        inputs = {
                "kernel-url": kernel_url,
                "selftests-url": selftests_url,
                "modules-url": modules_url,
                "build-id": build_id,
        }
        try:
            token = get_installation_token(secrets.get(self.__secrets_key),
                                           secrets.get(self.__client_id_key),
                                           self.__owner,
                                           self.__repo)
            github_post(self.__github_url, {"ref": "main", "inputs": inputs}, token)
        except Exception as e:
            logger.warning(f"Could not run GitHub action: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triggers kernel testing GitHub action")
    parser.add_argument("--kernel-url", required=True, help="Compiled kernel image url")
    parser.add_argument("--selftests-url", required=True, help="Compiled and compressed selftests url")
    parser.add_argument("--build-id", required=True, help="KernelCI build id")
    parser.add_argument("--secrets-key", required=True, help="Access token key inside secrets.json")
    args = parser.parse_args()
    runner = GitHubRunner(args.secrets_key, "CamilaAlvarez", "riscv-lab", "test_kernel.yml") 
    runner(args.kernel_url, args.selftests_url, args.build_id)

