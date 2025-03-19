import json
import requests
import logging
import argparse
from requests.adapters import HTTPAdapter, Retry
from config import secrets

logger = logging.getLogger(__name__)

def trigger_github_action(kernel_url, selftests_url, build_id):
    inputs = {
            "kernel-url": kernel_url,
            "selftests-url": selftests_url,
            "build-id": build_id,
    }
    headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {secrets.get('github_access_token')}",
            "X-GitHub-Api-Version": "2022-11-28"

    }
    s = requests.Session()
    retries = Retry(total=3,
                    backoff_factor=0.1,
                    status_forcelist=[429, 500, 502, 503, 504, 507])
    s.mount("https://api.github.com", HTTPAdapter(max_retries=retries))
    try:
        r = s.post("https://api.github.com/repos/CamilaAlvarez/riscv-lab/actions/workflows/test_kernel.yml/dispatches",
               data=json.dumps({"ref": "main", "inputs": inputs}).encode(),
               headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not trigger GitHub action: {str(e)}") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Triggers kernel testing GitHub action")
    parser.add_argument("--kernel-url", required=True, help="Compiled kernel image url")
    parser.add_argument("--selftests-url", required=True, help="Compiled and compressed selftests url")
    parser.add_argument("--build-id", required=True, help="KernelCI build id")
    args = parser.parse_args()
    trigger_github_action(args.kernel_url, args.selftests_url, args.build_id)
