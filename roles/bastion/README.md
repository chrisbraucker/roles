# Bastion

Host hardening role for systems exposed to the internet or other untrusted networks.


## Scope

- optional secondary SSH port handling
- optional SSH login notification via `sshrc`


## Notes

- this role is for host hardening policy, not generic ingress plumbing
- firewall implementation details belong in the `firewall` role
- internet-facing application routing belongs in roles such as `nginx`
- Fail2Ban installation and remediation behavior belong in the dedicated `fail2ban` role
- CrowdSec installation and remediation behavior belong in the dedicated `crowdsec` role
