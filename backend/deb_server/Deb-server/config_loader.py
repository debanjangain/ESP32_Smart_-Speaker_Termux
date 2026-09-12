import yaml
import os

class Config:
    _config = None

    @classmethod
    def load(cls, path="config_master.yaml"):
        if cls._config is None:
            with open(path, "r") as f:
                cls._config = yaml.safe_load(f)
        return cls._config

    @classmethod
    def get(cls, key_path, default=None):
        config = cls.load()
        keys = key_path.split(".")
        value = config
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default
        return value
