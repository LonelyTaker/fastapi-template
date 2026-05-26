import yaml
from typing import Any
from loguru import logger


class Configure:
    __config: dict = {}

    @classmethod
    def read_yaml(cls, path: str, encoding: str = r"utf-8"):
        with open(path, "r", encoding=encoding) as fp:
            config = yaml.safe_load(fp)
        logger.info(f"{config=}")
        cls.__config = config

    @classmethod
    def get(cls, *keys: str, default: Any = None) -> Any:
        _result = cls.__config
        for key in keys:
            if isinstance(_result, dict) and key in _result:
                _result = _result[key]
            else:
                return default
        return _result
