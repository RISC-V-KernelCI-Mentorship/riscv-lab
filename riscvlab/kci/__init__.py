import os
import yaml

_env = os.getenv("RISCV_ENV", "dev")

_base_dir = os.path.dirname(__file__)
_config_path = os.path.join(_base_dir, "kci-services.yml")

with open(_config_path, "r") as f:
    _config = yaml.safe_load(f)

BASE_URI = _config["events"][_env]
