from pathlib import Path

import yaml
from pydantic import BaseModel

from ipams.netbox import NetBoxConfig
from ipams.phpipam import PhpIpamConfig


class Config(BaseModel):
    netboxes: list[NetBoxConfig] = []
    phpipams: list[PhpIpamConfig] = []


def parse_config(config: Path) -> Config:
    '''Supports json or yaml config files'''
    if not config.exists():
        raise FileNotFoundError(f'Config file {config} does not exist')
    if config.suffix in ['.yaml', '.yml']:
        with open(config) as f:
            return Config.parse_obj(yaml.safe_load(f))
    return Config.parse_file(config)
