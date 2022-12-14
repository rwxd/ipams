# ipams - Query multiple IPAMs

## Install

### Pip

```bash
pip -U install ipams
```

### Pipx

```bash
pipx install ipams
```

Update

```bash
pipx upgrade ipams
```

## Supported IPAMs

- [NetBox](https://docs.netbox.dev/en/stable/) (wip)
- [phpIPAM](https://phpipam.net/) (wip)

### Planned


## Configuration

Save the configuration under `$HOME/.config/ipams/config.yml`
or use the `--config` flag to specify a different location.

```yaml
---
netboxes:
  - name: NetBox Demo
    url: https://demo.netbox.dev/
    token: 75d956ee746641e844f7fa26b63c6741d287c776

phpipams:
  - name: phpIPAM Demo
    url: https://demo.phpipam.net/
    app_id: ipams
    token: 75d956ee746641e844f7fa26b63c6741d287c776
    # Token OR username/password can be used
    # username: admin
    # password: admin
```

### Use the example config

```bash
mkdir -p $HOME/.config/ipams
cp config.yml $HOME/.config/ipams/config.yml
```

## Usage

### IP

```bash
❯ ipams ip 10.0.0.133
NetBox Demo
┏━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Address       ┃ Tenant ┃ VRF   ┃ Description ┃ Link                                           ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 10.0.0.133/27 │        │       │ test        │ https://demo.netbox.dev/ipam/ip-addresses/184/ │
├───────────────┼────────┼───────┼─────────────┼────────────────────────────────────────────────┤
│ 10.0.0.133/27 │        │ Alpha │             │ https://demo.netbox.dev/ipam/ip-addresses/191/ │
└───────────────┴────────┴───────┴─────────────┴────────────────────────────────────────────────┘
```

### Host

#### By name

```bash
❯ ipams host dmi01-akron
NetBox Demo
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Device            ┃ Site                 ┃ Tenant   ┃ Address ┃ Link                                     ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ dmi01-akron-pdu01 │ Dunder-Mifflin, Inc. │ DM-Akron │         │ https://demo.netbox.dev/dcim/devices/27/ │
├───────────────────┼──────────────────────┼──────────┼─────────┼──────────────────────────────────────────┤
│ dmi01-akron-rtr01 │ Dunder-Mifflin, Inc. │ DM-Akron │         │ https://demo.netbox.dev/dcim/devices/1/  │
├───────────────────┼──────────────────────┼──────────┼─────────┼──────────────────────────────────────────┤
│ dmi01-akron-sw01  │ Dunder-Mifflin, Inc. │ DM-Akron │         │ https://demo.netbox.dev/dcim/devices/14/ │
└───────────────────┴──────────────────────┴──────────┴─────────┴──────────────────────────────────────────┘
```

#### By IP

```bash
❯ ipams host 10.0.0.133
NetBox Demo
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Device             ┃ Site                 ┃ Tenant    ┃ Address       ┃ Link                                    ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ dmi01-nashua-rtr01 │ Dunder-Mifflin, Inc. │ DM-Nashua │ 10.0.0.133/27 │ https://demo.netbox.dev/dcim/devices/6/ │
└────────────────────┴──────────────────────┴───────────┴───────────────┴─────────────────────────────────────────┘
```

### Network

### By description

```bash
❯ ipams network "Shared"
NetBox Demo
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Network        ┃ Tenant ┃ VRF    ┃ Description     ┃ Link                                      ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 192.168.0.0/20 │        │ Shared │ Shared services │ https://demo.netbox.dev/ipam/prefixes/95/ │
└────────────────┴────────┴────────┴─────────────────┴───────────────────────────────────────────┘

```

### By IP

```bash
❯ ipams network 192.168.0.0/22
NetBox Demo
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Network        ┃ Tenant ┃ VRF    ┃ Description     ┃ Link                                      ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 192.168.0.0/22 │        │        │                 │ https://demo.netbox.dev/ipam/prefixes/73/ │
├────────────────┼────────┼────────┼─────────────────┼───────────────────────────────────────────┤
│ 192.168.0.0/20 │        │ Shared │ Shared services │ https://demo.netbox.dev/ipam/prefixes/95/ │
└────────────────┴────────┴────────┴─────────────────┴───────────────────────────────────────────┘
```
