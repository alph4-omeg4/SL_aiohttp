import pytoml as toml

CONFIG_PATH = "config/config.toml"


def load_config(path):
    with open(path) as f:
        config = toml.load(f)
    return config
