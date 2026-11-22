# Firewall

Host firewall baseline role. The current implementation targets `firewalld`.

## Scope

- install and enable `firewalld`
- remove `ufw` on Debian-family hosts
- apply the Red Hat initramfs workaround needed for firewalld module loading
- manage explicit firewalld ingress-port and forward-port rules

## Important Variables

- `firewall_backend`
  - currently expected to be `firewalld`
- `firewall_zone`
  - zone used for managed rules such as forward ports
- `firewall_enable_dhcpv6_client`
  - enables the `dhcpv6-client` service in the configured zone where appropriate
- `firewall_port_forwards`
  - structured forward-port rules rendered through `ansible.posix.firewalld`
- `firewall_open_ports`
  - structured ingress-port rules rendered through `ansible.posix.firewalld`

## Notes

- this role owns firewall implementation details so `bastion`, `nginx`, and `podman` can stay focused on their own domains
- firewalld forward-port rules apply to ingress through a zone-bound interface; they do not make `localhost` behave like external traffic
