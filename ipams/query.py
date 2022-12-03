from ipaddress import IPv4Address, IPv6Address
from pydantic import BaseModel
from typing import Union


class IPQuery(BaseModel):
    origin: str
    ip: Union[IPv4Address, IPv6Address]
    description: str
    link: str

    def __str__(self):
        return f"{self.ip} - {self.description} - {self.link}"
