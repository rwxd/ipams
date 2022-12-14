import typer
from ipaddress import ip_address, ip_network
from pathlib import Path
from ipams.config import parse_config
from rich.console import Console

app = typer.Typer()
console = Console()

default_config_path = Path.home().joinpath('.config/ipams/config.yml')


@app.command()
def ip(
    ip: str = typer.Argument(..., help="IP address"),
    config: Path = typer.Option(
        default_config_path, "--config", "-c", help="Path to config file"
    ),
):
    converted = ip_address(ip)
    parsed_config = parse_config(config)
    for nb in parsed_config.netboxes:
        table = nb.query_ip(converted)
        if len(table.columns) > 0:
            console.print(table)

    for phpipam in parsed_config.phpipams:
        table = phpipam.query_ip(converted)
        if len(table.columns) > 0:
            console.print(table)


@app.command()
def host(
    query: str = typer.Argument(..., help="Host name or ip address"),
    config: Path = typer.Option(
        default_config_path, "--config", "-c", help="Path to config file"
    ),
):
    parsed_config = parse_config(config)
    for nb in parsed_config.netboxes:
        try:
            ip = ip_address(query)
            table = nb.query_host_by_ip(ip)
        except ValueError:
            table = nb.query_host_by_name(query)
        if len(table.columns) > 0:
            console.print(table)


@app.command()
def network(
    query: str = typer.Argument(..., help="Network name or address"),
    config: Path = typer.Option(
        default_config_path, "--config", "-c", help="Path to config file"
    ),
):
    parsed_config = parse_config(config)
    for nb in parsed_config.netboxes:
        try:
            address = ip_network(query)
            table = nb.query_network_by_address(address)
        except ValueError:
            table = nb.query_network_by_string(query)
        if len(table.columns) > 0:
            console.print(table)
