import importlib.metadata
from ipaddress import ip_address, ip_network
from pathlib import Path

import typer
from rich.console import Console

from ipams.config import parse_config
from ipams.netbox import NetBoxConnector
from ipams.phpipam import PhpIpamConnector

app = typer.Typer()
console = Console()

default_config_path = Path.home().joinpath('.config/ipams/config.yml')


@app.command()
def ip(
    ip: str = typer.Argument(..., help='IP address'),
    config: Path = typer.Option(
        default_config_path, '--config', '-c', help='Path to config file'
    ),
):
    '''
    Query IPAMs for IP address
    '''
    converted = ip_address(ip)
    parsed_config = parse_config(config)
    for nb in parsed_config.netboxes:
        table = NetBoxConnector(nb).query_ip(converted)
        if len(table.rows) > 0:
            console.print(table)

    for phpipam in parsed_config.phpipams:
        table = PhpIpamConnector(phpipam).query_ip(converted)
        if len(table.rows) > 0:
            console.print(table)


@app.command()
def host(
    query: str = typer.Argument(..., help='Host name or ip address'),
    config: Path = typer.Option(
        default_config_path, '--config', '-c', help='Path to config file'
    ),
):
    '''
    Query IPAMs for host name or IP address
    '''
    parsed_config = parse_config(config)
    ip = None
    try:
        ip = ip_address(query)
    except ValueError:
        pass

    for nb in parsed_config.netboxes:
        if ip:
            table = NetBoxConnector(nb).query_host_by_ip(ip)
        else:
            table = NetBoxConnector(nb).query_host_by_name(query)
        if len(table.rows) > 0:
            console.print(table)

    for phpipam in parsed_config.phpipams:
        if ip:
            table = PhpIpamConnector(phpipam).query_host_by_ip(ip)
        else:
            table = PhpIpamConnector(phpipam).query_host_by_name(query)
        if len(table.rows) > 0:
            console.print(table)


@app.command()
def network(
    query: str = typer.Argument(..., help='Network name or address'),
    config: Path = typer.Option(
        default_config_path, '--config', '-c', help='Path to config file'
    ),
):
    '''
    Query IPAMs for network name or address
    '''
    parsed_config = parse_config(config)
    subnet = None
    try:
        subnet = ip_network(query)
    except ValueError:
        subnet = None

    for nb in parsed_config.netboxes:
        if subnet:
            table = NetBoxConnector(nb).query_network_by_address(subnet)
        else:
            table = NetBoxConnector(nb).query_network_by_string(query)
        if len(table.rows) > 0:
            console.print(table)

    for phpipam in parsed_config.phpipams:
        if subnet:
            table = PhpIpamConnector(phpipam).query_network_by_address(subnet)
        else:
            table = PhpIpamConnector(phpipam).query_network_by_string(query)
        if len(table.rows) > 0:
            console.print(table)


@app.command()
def subnet(
    query: str = typer.Argument(..., help='Subnet CIDR to query hosts from'),
    config: Path = typer.Option(
        default_config_path, '--config', '-c', help='Path to config file'
    ),
):
    '''
    Query IPAMs for hosts in a subnet
    '''
    cidr = ip_network(query)
    parsed_config = parse_config(config)
    for nb in parsed_config.netboxes:
        table = NetBoxConnector(nb).query_subnet_by_cidr(cidr)
        if len(table.rows) > 0:
            console.print(table)


@app.command()
def version():
    console.print(importlib.metadata.version('ipams'))
