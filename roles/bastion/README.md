# Bastion

Host hardening role for systems exposed to the internet or other untrusted networks.

## Scope

- fail2ban baseline
- optional secondary SSH port handling
- optional SSH login notification via `sshrc`
- future CrowdSec integration, currently gated off by default

## Notes

- this role is for host hardening policy, not generic ingress plumbing
- firewall implementation details belong in the `firewall` role
- internet-facing application routing belongs in roles such as `nginx`
