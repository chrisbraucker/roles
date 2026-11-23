# Certbot

Containerized certbot role built on Quadlet and systemd timers.

## Entry Points

- `main`
  - deploys the renewal container, post-success reload hook, and timer
- `certificates`
  - issues or updates certificate lineages from structured certificate objects
- `http_01`
  - prepares the shared ACME webroot for HTTP-01 challenges
- `dns_01`
  - supplies provider credentials as a Podman secret and passes provider-specific Certbot arguments

## Model

- renewal runs in a Quadlet-managed oneshot container
- a systemd timer triggers the renewal service
- certificate issuance is explicit through `tasks_from: certificates.yml`
- direct certificate issuance does not reload a dependent service; callers should do so after deploying that service
- the post-success hook reloads the dependent service after scheduled renewal runs

## Important Variables

- `certbot_image_repo`
- `certbot_image_ref`
- `certbot_service_name`
- `certbot_challenge_type`
- `certbot_dns_01_credentials`
- `certbot_dns_01_args`
- `certbot_certificates`
- `certbot_config_dir`
- `certbot_work_dir`
- `certbot_logs_dir`
- `certbot_http_01_webroot`
- `certbot_reload_service_name`
- `nginx_container_gid`

## Certificate Objects

`certbot_certificates` entries should define:

- `name`
- `domains`

Optional per-certificate overrides:

- `server`
- `key_type`

## DNS-01

DNS-01 accepts provider credentials as `certbot_dns_01_credentials` and stores them as a Podman secret for both issuance and renewal.
The secret is available inside the container at `/run/secrets/certbot-dns-credentials`.
Put only plugin flags and paths in `certbot_dns_01_args`; keep token and key values in Ansible Vault.

For example, with the Cloudflare plugin image:

```yaml
certbot_challenge_type: 'dns_01'
certbot_image_repo: 'docker.io/certbot/dns-cloudflare'
certbot_dns_01_credentials: |
  dns_cloudflare_api_token = {{ vault_certbot_cloudflare_token }}
certbot_dns_01_args:
  - '--dns-cloudflare'
  - '--dns-cloudflare-credentials'
  - '/run/secrets/certbot-dns-credentials'
  - '--dns-cloudflare-propagation-seconds'
  - '60'
```

## Notes

- by default the role does not force an ACME directory URL; certbot uses its own default server selection unless `certbot_server` or `item.server` is set
- HTTP-01 support is infrastructure-level and intended to work with the nginx role's global HTTP redirect server
- when `nginx_container_gid` is set, certificate issuance and the post-success hook adjust group ownership and permissions under `live/` and `archive/` so nginx can read certbot-managed keys and certificate material
