# CrowdSec

Host-local CrowdSec deployment role for the security engine and firewall bouncer.

## Scope

- install the CrowdSec engine
- install the nftables firewall bouncer
- bootstrap the CrowdSec package repository on RedHat-family hosts
- register the firewall bouncer against the local API
- render acquisition snippets

## Current Model

- host-local engine
- host-local local API
- host-local firewall bouncer

This is the pragmatic single-host deployment model. It is the right first step before introducing a split between agents, a central LAPI, and distributed bouncers.

## Important Variables

- `crowdsec_log_media`
- `crowdsec_log_level`
- `crowdsec_lapi_listen_uri`
- `crowdsec_lapi_trusted_ips`
- `crowdsec_lapi_prometheus_enabled`
- `crowdsec_lapi_prometheus_level`
- `crowdsec_lapi_prometheus_listen_addr`
- `crowdsec_lapi_prometheus_listen_port`
- `crowdsec_manage_repo`
- `crowdsec_collections`
- `crowdsec_nginx_journald_enabled`
- `crowdsec_nginx_journald_units`
- `crowdsec_acquisitions`
- `crowdsec_firewall_bouncer_package`
- `crowdsec_firewall_bouncer_name`
- `crowdsec_firewall_bouncer_api_url`
- `crowdsec_firewall_bouncer_api_key`
- `crowdsec_firewall_bouncer_mode`
- `crowdsec_firewall_bouncer_nftables_ipv4_priority`
- `crowdsec_firewall_bouncer_nftables_ipv6_priority`
- `crowdsec_firewall_bouncer_nftables_hooks`

## Notes

- the role currently bootstraps the CrowdSec package repository on RedHat-family hosts only
- the role renders `config.yaml.local` and `local_api_credentials.yaml.local` overrides for the local API and logging behavior
- the firewall bouncer uses a `.yaml.local` override file under `/etc/crowdsec/bouncers/`
- if an API key is not provided explicitly, the role reuses the key from an existing local override or generates a new one with `cscli`
- nginx integration currently assumes journald acquisition if you enable `crowdsec_nginx_journald_enabled`
- the role defaults the CrowdSec nftables chain priority to `20`, so firewalld can enforce host exposure policy first and CrowdSec can apply reputation-based drops afterwards
