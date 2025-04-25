import yaml
import os
from runners.github import GitHubRunner
from runners.riscv_api import RiscVAPIRunner


_runners = []
_dirname = os.path.dirname(os.path.abspath(__file__))

def _get_key_or_raise(key, runner, runner_type):
    if key not in runner:
        raise Exception(f"Missing required field {key} for runner {runner_type}")
    return runner[key]

def _create_github_runner(runner, runner_type):
    owner = _get_key_or_raise("owner", runner, runner_type)
    repo = _get_key_or_raise("repo", runner, runner_type)
    workflow_id = _get_key_or_raise("workflow-id", runner, runner_type)
    secrets_key = _get_key_or_raise("secrets-key", runner, runner_type)
    client_id_key = _get_key_or_raise("client-id-key", runner, runner_type)
    return GitHubRunner(secrets_key, owner, repo, workflow_id, client_id_key)

def _create_riscv_api_runner(runner, runner_type):
    url = _get_key_or_raise("url", runner, runner_type)
    tests = _get_key_or_raise("tests", runner, runner_type)
    tests_collection = _get_key_or_raise("test-collection", runner, runner_type)
    return RiscVAPIRunner(url, tests, tests_collection)


def run_event_processing(kernel_image, selftests, modules, build_id):
    for runner in _runners:
        runner(kernel_image, selftests, modules, build_id)

with open(os.getenv("RUNNERS"), "r") as f:
    _yaml_runners = yaml.safe_load(f)

for runner in _yaml_runners["runners"]:
    if "type" not in runner:
        raise Exception("Missing runner type")
    runner_type = runner["type"]
    if runner_type == "github":
        _runners.append(_create_github_runner(runner, runner_type))
    elif runner_type == "riscv-api":
        _runners.append(_create_riscv_api_runner(runner, runner_type))
    else:
        raise Exception(f"Invalid runner type: {runner_type}")


