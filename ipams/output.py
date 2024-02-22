from rich.style import Style
from rich.table import Table


class DefaultNetBoxTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'NetBox'
        self.title_justify = 'left'
        self.title_style = Style(bold=True, underline=True)
        self.expand = False
        self.highlight = True
        self.show_lines = True


class NetBoxIPTable(DefaultNetBoxTable):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Address', justify='left', style='magenta', no_wrap=True)
        self.add_column('Tenant', justify='left', style='magenta')
        self.add_column('Hostname', justify='left', style='magenta', no_wrap=True)
        self.add_column('VRF', justify='left', style='magenta')
        self.add_column('Description', justify='left', style='green')
        self.add_column('Link', justify='left', style='green')

    def add_row(
        self,
        vrf: str,
        tenant: str,
        address: str,
        hostname: str,
        description: str,
        link: str,
    ):
        super().add_row(address, hostname, tenant, vrf, description, link)


class NetBoxHostTable(DefaultNetBoxTable):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Device', justify='left', style='magenta', no_wrap=True)
        self.add_column('Site', justify='left', style='magenta')
        self.add_column('Tenant', justify='left', style='magenta')
        self.add_column('Address', justify='left', style='magenta', no_wrap=True)
        self.add_column('Link', justify='left', style='green')

    def add_row(
        self,
        device: str,
        tenant: str,
        site: str,
        address: str,
        link: str,
    ):
        super().add_row(device, tenant, site, address, link)


class NetBoxNetworkTable(DefaultNetBoxTable):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Network', justify='left', style='magenta', no_wrap=True)
        self.add_column('Tenant', justify='left', style='magenta')
        self.add_column('VRF', justify='left', style='magenta')
        self.add_column('Description', justify='left', style='green')
        self.add_column('Link', justify='left', style='green')

    def add_row(self, vrf: str, tenant: str, network: str, description: str, link: str):
        super().add_row(network, tenant, vrf, description, link)


class NetBoxSubnetTable(NetBoxHostTable):
    pass


class DefaultPhpIpam(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = 'PHP IPAM'
        self.title_justify = 'left'
        self.title_style = Style(bold=True, underline=True)
        self.expand = False
        self.highlight = True
        self.show_lines = True


class PhpIpamIpTable(DefaultPhpIpam):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Address', justify='left', style='magenta', no_wrap=True)
        self.add_column('Section', justify='left', style='magenta')
        self.add_column('Hostname', justify='left', style='magenta', no_wrap=True)
        self.add_column('Description', justify='left', style='green')
        self.add_column('Link', justify='left', style='green', no_wrap=True)

    def add_row(
        self, address: str, hostname: str, section: str, description: str, link: str
    ):
        super().add_row(address, section, hostname, description, link)


class PhpIpamHostTable(DefaultPhpIpam):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Hostname', justify='left', style='magenta', no_wrap=True)
        self.add_column('Section', justify='left', style='magenta')
        self.add_column('Address', justify='left', style='magenta', no_wrap=True)
        self.add_column('Description', justify='left', style='green')
        self.add_column('Link', justify='left', style='green', no_wrap=True)

    def add_row(
        self, address: str, hostname: str, section: str, description: str, link: str
    ):
        super().add_row(hostname, section, address, description, link)


class PhpIpamNetworkTable(DefaultPhpIpam):
    def __init__(self, name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = name
        self.add_column('Network', justify='left', style='magenta', no_wrap=True)
        self.add_column('Section', justify='left', style='magenta')
        self.add_column('Description', justify='left', style='green')
        self.add_column('Link', justify='left', style='green', no_wrap=True)

    def add_row(self, network: str, section: str, description: str, link: str):
        super().add_row(network, section, description, link)
