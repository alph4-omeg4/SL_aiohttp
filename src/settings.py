import pathlib
import pytoml as toml

BASE_DIR = pathlib.Path(__file__).parent
CONFIG_PATH = f"{BASE_DIR}/config/config.toml"


def load_config(path):
    with open(path) as f:
        config = toml.load(f)
    return config
