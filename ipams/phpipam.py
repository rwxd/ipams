from ipaddress import IPv4Address, IPv4Network, IPv6Address, IPv6Network
from typing import Literal, Optional, Union

import requests
from pydantic import BaseModel

from ipams.logging import logger
from ipams.output import PhpIpamHostTable, PhpIpamIpTable, PhpIpamNetworkTable

_phpipamauth = Literal['password', 'token']


class PhpIpamConfig(BaseModel):
    """Configuration for PhpIpam API"""

    name: str
    url: str
    app_id: str
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    verify_ssl: bool = True


class PhpIpamConnector:
    def __init__(self, config: PhpIpamConfig):
        self.name = config.name
        self.url = config.url
        self.app_id = config.app_id
        self.username = config.username
        self.password = config.password
        self.token = config.token
        self.verify_ssl = config.verify_ssl

        self.api_url = f'{self.url.rstrip("/")}/api/{self.app_id}'

        self.auth_method: _phpipamauth = 'token'
        if not self.token:
            self.auth_method = 'password'

        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        session = requests.Session()
        session.verify = self.verify_ssl

        session.headers.update({'Content-Type': 'application/json'})
        session.headers.update({'phpipam-token': self._get_token()})
        return session

    def _get_token(self) -> str:
        if self.auth_method == 'password':
            return self._get_token_password()
        elif self.token and self.auth_method == 'token':
            return self.token
        else:
            raise ValueError('Invalid auth method')

    def _get_token_password(self) -> str:
        url = f'{self.api_url}/user/'
        logger.debug(f'Post "{url}"')
        response = self.session.post(
            url,
            headers={'Content-Type': 'application/json'},
            auth=(self.username or '', self.password or ''),
        )
        response.raise_for_status()
        data = response.json()
        if data['code'] != 200 or data['success'] is not True:
            print(data)
            raise ValueError('Invalid credentials')
        return data['data']['token']

    def get(self, endpoint: str, params: dict = {}) -> requests.Response:
        url = f'{self.api_url}/{endpoint}'
        logger.debug(f'Get "{url}" with params: {params}')
        response = self.session.get(url, params=params)
        return response

    def post(self, endpoint: str, data: dict = {}) -> requests.Response:
        url = f'{self.api_url}/{endpoint}'
        logger.debug(f'Post "{url}" with json: {data}')
        response = self.session.post(url, json=data)
        return response

    def get_paged(
        self,
    ) -> list[dict]:
        return []

    def query_ip(self, ip: Union[IPv4Address, IPv6Address]) -> PhpIpamIpTable:
        results = PhpIpamIpTable(self.name)
        response = self.get(f'/addresses/search/{str(ip)}/')
        if response.status_code == 404:
            return results
        data = response.json()
        for address in data['data']:
            subnet_id = address['subnetId']
            section = self._get_section_for_subnet(subnet_id)
            results.add_row(
                address=address['ip'],
                hostname=address['hostname'],
                section=section['name'],
                description=address['description'],
                link=self._build_link(
                    f'/subnets/{section["id"]}/{subnet_id}/address-details/{address["id"]}'
                ),
            )
        return results

    def query_host_by_name(self, hostname: str) -> PhpIpamHostTable:
        results = PhpIpamHostTable(self.name)
        response = self.get(f'/addresses/search_hostbase/{hostname}/')
        if response.status_code == 404:
            return results
        data = response.json()
        for address in data['data']:
            subnet_id = address['subnetId']
            section = self._get_section_for_subnet(subnet_id)
            results.add_row(
                address=address['ip'],
                hostname=address['hostname'],
                section=section['name'],
                description=address['description'],
                link=self._build_link(
                    f'/subnets/{section["id"]}/{subnet_id}/address-details/{address["id"]}'
                ),
            )
        return results

    def query_network_by_address(
        self, address: Union[IPv4Network, IPv6Network]
    ) -> PhpIpamNetworkTable:
        results = PhpIpamNetworkTable(self.name)
        response = self.get(f'/subnets/search/{str(address)}/')
        if response.status_code == 404:
            return results
        data = response.json()
        for subnet in data['data']:
            section = self._get_section_for_subnet(subnet['id'])
            results.add_row(
                network=subnet['subnet'] + '/' + subnet['mask'],
                description=subnet['description'],
                section=section['name'],
                link=self._build_link(f'/subnets/{section["id"]}/{subnet["id"]}/'),
            )
        return results

    def query_network_by_string(self, query: str) -> PhpIpamNetworkTable:
        results = PhpIpamNetworkTable(self.name)
        response = self.get('/subnets/')
        if response.status_code == 500:
            logger.warning(f'Query on phpipam "{self.name}" failed with error code 500')
            logger.warning('Please take a look in the phpipam server error log')
            return results
        elif response.status_code != 200:
            return results
        data = response.json()
        for subnet in data['data']:
            if subnet['description'] and query.lower() in subnet['description'].lower():
                section = self._get_section_for_subnet(subnet['id'])
                results.add_row(
                    network=subnet['subnet'] + '/' + subnet['mask'],
                    description=subnet['description'],
                    section=section['name'],
                    link=self._build_link(f'/subnets/{section["id"]}/{subnet["id"]}/'),
                )
        return results

    def query_host_by_ip(self, ip: Union[IPv4Address, IPv6Address]) -> PhpIpamIpTable:
        return self.query_ip(ip)

    def _get_section(self, section: int) -> dict:
        endpoint = f'/sections/{section}/'
        response = self.get(endpoint)
        return response.json()['data']

    def _get_subnet(self, subnet_id: int) -> dict:
        endpoint = f'/subnets/{subnet_id}/'
        response = self.get(endpoint)
        return response.json()['data']

    def _get_section_for_subnet(self, subnet_id: int) -> dict:
        subnet = self._get_subnet(subnet_id)
        return self._get_section(subnet['sectionId'])

    def _build_link(self, extra: str) -> str:
        return f'{self.url.rstrip("/")}/{extra.lstrip("/")}'
