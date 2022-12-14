from ipaddress import IPv4Address, IPv6Address
import requests
from typing import Optional, Literal, Union
from ipams.logging import logger
from ipams.output import PhpIpamIpTable
from pydantic import BaseModel
from functools import lru_cache

_phpipamauth = Literal['password', 'token']


class PhpIpamConnector(BaseModel):
    name: str
    url: str
    username: Optional[str] = None
    password: Optional[str] = None
    app_id: Optional[str] = None
    token: Optional[str] = None
    verify_ssl: bool = True
    api_url = ''
    auth_method: _phpipamauth = 'token'
    session: Optional[requests.Session] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_url = f'{self.url.rstrip("/")}/api/{self.app_id}'

        if not self.token:
            self.auth_method: _phpipamauth = 'password'
        else:
            self.auth_method: _phpipamauth = 'token'

        if not self.session:
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
        response.raise_for_status()
        return response

    def post(self, endpoint: str, data: dict = {}) -> requests.Response:
        url = f'{self.api_url}/{endpoint}'
        logger.debug(f'Post "{url}" with json: {data}')
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response

    def get_paged(
        self,
    ) -> list[dict]:
        return []

    def query_ip(self, ip: Union[IPv4Address, IPv6Address]) -> PhpIpamIpTable:
        results = PhpIpamIpTable(self.name)
        response = self.get(f'/addresses/search/{str(ip)}/')
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
