# Fail2Ban

Host-local Fail2Ban role for fast journald-backed bans with nftables enforcement.


## Scope

- install Fail2Ban
- render a role-owned `jail.d` drop-in
- enforce bans through nftables
- watch nginx via journald
- optionally keep an `sshd` jail


## Current Model

- host-local service
- journald backend
- nftables-based banning
- nginx-focused jails by default

This role is intended to complement `crowdsec`, not replace it. The pragmatic split is fast local reactions in Fail2Ban and broader scenario/reputation handling in CrowdSec.


## Important Variables

- `fail2ban_backend`
- `fail2ban_banaction`
- `fail2ban_nftables_table`
- `fail2ban_nftables_chain`
- `fail2ban_nftables_chain_hook`
- `fail2ban_nftables_chain_priority`
- `fail2ban_nftables_blocktype`
- `fail2ban_ignore_ips_default`
- `fail2ban_ignore_ips`
- `fail2ban_nginx_enabled`
- `fail2ban_nginx_journalmatch`
- `fail2ban_nginx_http_auth_enabled`
- `fail2ban_nginx_limit_req_enabled`
- `fail2ban_nginx_botsearch_enabled`
- `fail2ban_nginx_bad_request_enabled`
- `fail2ban_nginx_forbidden_enabled`
- `fail2ban_sshd_enabled`


## Notes

- the role uses the `systemd` backend by default because nginx logs are expected to land in journald
- the default banaction is `nftables`
- the default nftables chain priority is `20`, which places Fail2Ban after `firewalld` and before the current CrowdSec defaults in this repo
- the nginx `limit_req` jail is only useful if nginx actually logs rate limiting events, which this repo now does via `limit_req_log_level`
- keep jails narrow and high-confidence; let CrowdSec handle the broader scenario set
