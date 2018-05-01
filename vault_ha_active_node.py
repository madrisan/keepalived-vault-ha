#!/usr/bin/env python3

'''Keepalived Tracking Script for HashiCorp Vault HA.

This simple Python script can be used as a Keepalived tracking script for
monitoring an HashiCorp Vault HA cluster and setup a VIP on the active Vault
node.

GitHub Site:
    https://github.com/madrisan/keepalived-vault-ha

This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
'''

__author__ = "Davide Madrisan <davide.madrisan.gmail.com>"
__copyright__ = "Copyright (C) 2018 Davide Madrisan"
__license__ = "GPL-3.0"
__status__ = "Production"
__version__ = "2"

import argparse
import logging
import os
import requests
import sys

def parse_args():
    '''This function parses and return arguments passed in'''

    progname = os.path.basename(sys.argv[0])
    default_timeout = 3

    parser = argparse.ArgumentParser(
        description = 'Keepalived Tracking Script for HashiCorp Vault HA.')
    parser.add_argument(
        "-d", "--debug",
        action = "store_true",
        help = "execute this script in debug mode",
        dest = "debug")
    parser.add_argument(
        "-t", "--timeout",
        help = "stop waiting for a response after a given number of seconds"
               " (default: {0})".format(default_timeout),
        dest = "timeout",
        default = default_timeout,
        type = float)
    parser.add_argument(
        "--version", action = "version",
        version = "{0} v{1}"
                  " ( https://github.com/madrisan/keepalived-vault-ha )"
                  .format(progname, __version__))

    return parser.parse_args()

def check_vault(timeout):
    '''This function returns True if the node pointed by the environment variable
       VAULT_ADDR is active, False otherwise.'''

    api_version = 'v1'
    resource = 'sys/leader'

    vault_addr = os.getenv('VAULT_ADDR', '')
    if not vault_addr:
        logging.debug('VAULT_ADDR is unset, aborting...')
        return False

    logging.debug('VAULT_ADDR: {0}'.format(vault_addr))

    leader_url = ('{0}/{1}/{2}'
                  .format(vault_addr, api_version, resource))
    logging.debug('Querying the URL: {0}'.format(leader_url))

    try:
        r = requests.get(leader_url, timeout=timeout)
        if r.status_code != 200:
            logging.debug('requests returned with status code {0}'.format(r.status_code))
            return False
        ha_enabled = r.get('ha_enabled', False)
        is_self = r.get('is_self', False)
        if ha_enabled and is_self:
            return True
    except requests.exceptions.RequestException as e:
        logging.error(format(str(e)))

    return False

if __name__ == '__main__':
    args = parse_args()
    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    is_active = check_vault(args.timeout)
    sys.exit(0 if is_active else 1)
