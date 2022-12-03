from pynetbox.core.api import Api
from typing import Union
from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from ipams.query import IPQuery
from pydantic import BaseModel
from ipams.output import NetBoxHostTable, NetBoxIPTable, NetBoxNetworkTable


class NetBoxConnector(BaseModel):
    name: str
    url: str
    token: str
    threading: bool = True
    verify_ssl: bool = True

    @property
    def conn(self) -> Api:
        return Api(self.url, token=self.token, threading=True)

    def query_ip(self, ip: Union[IPv4Address, IPv6Address]) -> NetBoxIPTable:
        """Query NetBox for IP address"""
        results = NetBoxIPTable(self.name)
        for q_ip in self.conn.ipam.ip_addresses.filter(q=str(ip)):
            results.add_row(
                vrf=q_ip.vrf.name if q_ip.vrf else "",
                tenant=q_ip.tenant.name if q_ip.tenant else "",
                address=str(q_ip.address),
                description=str(q_ip.description),
                link=f"{self.url.rstrip('/')}/ipam/ip-addresses/{q_ip.id}/",
            )
        return results

    def query_host_by_ip(self, ip: Union[IPv4Address, IPv6Address]) -> NetBoxHostTable:
        results = NetBoxHostTable(self.name)
        for q_ip in self.conn.ipam.ip_addresses.filter(
            q=str(ip), assigned_to_interface=True
        ):
            if q_ip.assigned_object and q_ip.assigned_object.device:
                device = self.conn.dcim.devices.get(id=q_ip.assigned_object.device.id)
                if device:
                    results.add_row(
                        tenant=device.tenant.name if device.tenant else "",
                        site=device.site.name if device.site else "",
                        device=device.name,
                        address=str(q_ip.address),
                        link=f"{self.url.rstrip('/')}/dcim/devices/{device.id}/",
                    )
        return results

    def query_host_by_name(self, name: str) -> NetBoxHostTable:
        results = NetBoxHostTable(self.name)
        for device in self.conn.dcim.devices.filter(q=name):
            results.add_row(
                tenant=device.tenant.name if device.tenant else "",
                site=device.site.name if device.site else "",
                device=device.name,
                address=str(device.primary_ip.address if device.primary_ip4 else ""),
                link=f"{self.url.rstrip('/')}/dcim/devices/{device.id}/",
            )
        return results

    def query_network_by_address(
        self, network: Union[IPv4Network, IPv6Network]
    ) -> NetBoxNetworkTable:
        results = NetBoxNetworkTable(self.name)
        for q_network in self.conn.ipam.prefixes.filter(q=str(network)):
            results.add_row(
                network=str(q_network.prefix),
                vrf=q_network.vrf.name if q_network.vrf else "",
                tenant=q_network.tenant.name if q_network.tenant else "",
                description=str(q_network.description),
                link=f"{self.url.rstrip('/')}/ipam/prefixes/{q_network.id}/",
            )
        return results

    def query_network_by_string(self, query: str) -> NetBoxNetworkTable:
        results = NetBoxNetworkTable(self.name)
        for q_network in self.conn.ipam.prefixes.filter(q=query):
            results.add_row(
                network=str(q_network.prefix),
                vrf=q_network.vrf.name if q_network.vrf else "",
                tenant=q_network.tenant.name if q_network.tenant else "",
                description=str(q_network.description),
                link=f"{self.url.rstrip('/')}/ipam/prefixes/{q_network.id}/",
            )
        return results
