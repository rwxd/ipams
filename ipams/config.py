from pathlib import Path
from pydantic import BaseModel
import yaml
from ipams.netbox import NetBoxConnector


class NetBox(BaseModel):
    url: str
    token: str


class PhpIPAMs(BaseModel):
    url: str
    token: str
    app_id: str


class Config(BaseModel):
    netboxes: list[NetBoxConnector] = []
    phpipams: list[PhpIPAMs] = []


def parse_config(config: Path) -> Config:
    '''Supports json or yaml config files'''
    if not config.exists():
        raise FileNotFoundError(f"Config file {config} does not exist")
    if config.suffix in [".yaml", ".yml"]:
        with open(config, 'r') as f:
            return Config.parse_obj(yaml.safe_load(f))
    return Config.parse_file(config)
