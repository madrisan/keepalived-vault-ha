#!/usr/bin/env python3

"""Tracking script for HashiCorp Vault HA Cluster.

This simple Python script can be used as a tracking script for monitoring
an HashiCorp Vault HA cluster and setup a VIP on the active Vault node.

GitHub Site:
    https://github.com/madrisan/keepalived-vault-ha
"""

__author__ = "Davide Madrisan <davide.madrisan.gmail.com>"
__copyright__ = "Copyright 2018 Davide Madrisan"
__license__ = "GPL-3.0"
__status__ = "Stable"
__version__ = "1"

from os import getenv
import requests
import sys

def main():
    api_version = 'v1'
    resource = 'sys/leader'

    vault_addr = getenv('VAULT_ADDR', '')
    if not vault_addr:
        sys.exit(1)

    leader_url = '{0}/{1}/{2}'.format(vault_addr, api_version, resource)

    try:
        r = requests.get(leader_url)
        if r.status_code != 200:
            sys.exit(1)

        ha_enabled = r.get('ha_enabled', False)
        is_self = r.get('is_self', False)
        if ha_enabled and is_self:
            sys.exit(0)
    except:
        pass

    sys.exit(1)

if __name__ == '__main__':
    main()
