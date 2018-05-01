# Keepalived Vault HA

### Keepalived Tracking Script for HashiCorp Vault HA

To avoid a single point of failure with your [HashiCorp Vault] infrastructure,
one would set up Vault in *High Availability Mode* (HA) with two identical Vault
instances (one *active* and one *standby*) and use [Keepalived] to run *VRRP*
between them.

*VRRP* provides a *virtual IP* address to the *active* Vault HA, and transfers
the Virtual IP to the standby Vault HA in case of failure.

##### What is a Virtual IP Address? 

Network interface cards (*NICs*) typically bind to a single IP address in TCP/IP
networks. However, you can also tell the NIC to listen on extra addresses.
Such addresses are called *virtual IP addresses* or *VIPs* for short.

##### Keepalived Trancking Scripts

You can configure a VIP address by using a *tracking script*, that is a program
that Keepalived runs at regular intervals, according to a *vrrp_script*
definition:

```
vrrp_script vault_active_node_script {
  script       "program_path arg ..."
  interval i   # Run script every i seconds
  fall f       # If script returns non-zero f times in succession, enter FAULT state
  rise r       # If script returns zero r times in succession, exit FAULT state
  timeout t    # Wait up to t seconds for script before assuming non-zero exit code
  weight w     # Reduce priority by w on fall
}
```

*program_path* is the full pathname of an executable script or binary
(*vault_ha_active_node.py* in our case, for instance *script* can point to
`/usr/local/bin/vault_ha_active_node.py`).

You can use tracking scripts with a *vrrp_instance* section by specifying a 
*track_script clause*, for example:

```
vrrp_instance VIP_VAULT_HA {
  state MASTER
  interface ens192
  virtual_router_id 25
  priority 100
  advert_int 1
  authentication {
    auth_type PASS
    auth_pass n0ts0r4nd0mp4ssw0rd
  }
  virtual_ipaddress {
    10.0.0.100/24
  }
  track_script {
    vault_active_node_script
  }
}
```

##### The Tracking Script *vault_ha_active_node.py*

The Python3 script `vault_ha_active_node.py` looks at the environment variable
`VAULT_ADDR` and when set do ask the Vault REST API if the (local) Vault node is
the active one. In that case will return `0`.
The script will return `1` otherwise (`VAULT_ADDR` unset, vault service not
running or running but not unsealed, node in standby mode, a generic error).

The script requires the Python library `requests` (provided by the package
`python3-requests` in Debian and Fedora).

[HashiCorp Vault]: https://www.vaultproject.io/
[Keepalived]: http://www.keepalived.org/
