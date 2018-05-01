#!/usr/bin/env python3

from os import getenv
import requests

def main():
    api_version = 'v1'
    resource = 'sys/leader'

    vault_addr = getenv('VAULT_ADDR', '')
    if not vault_addr:
        return 1

    leader_url = '{0}/{1}/{2}'.format(vault_addr, api_version, resource)

    try:
        r = requests.get(leader_url)
        if r.status_code != 200:
            return 1

        ha_enabled = r.get('ha_enabled', False)
        is_self = r.get('is_self', False)
        if ha_enabled and is_self:
            return 0
    except:
        pass

    return 1

if __name__ == '__main__':
    main()
