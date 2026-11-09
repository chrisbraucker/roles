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
  - mounts a provider credentials file and passes provider-specific Certbot arguments

## Model

- renewal runs in a Quadlet-managed oneshot container
- a systemd timer triggers the renewal service
- certificate issuance is explicit through `tasks_from: certificates.yml`
- nginx or another dependent service can be reloaded via a post-success service hook

## Important Variables

- `certbot_image_repo`
- `certbot_image_ref`
- `certbot_service_name`
- `certbot_challenge_type`
- `certbot_dns_01_credentials_file`
- `certbot_dns_01_args`
- `certbot_certificates`
- `certbot_config_dir`
- `certbot_work_dir`
- `certbot_logs_dir`
- `certbot_http_01_webroot`
- `certbot_reload_service_name`

## Certificate Objects

`certbot_certificates` entries should define:

- `name`
- `domains`

Optional per-certificate overrides:

- `server`
- `key_type`

## DNS-01

DNS-01 uses an externally managed credentials file and a provider-specific Certbot image and argv.
The credentials file must be outside `certbot_config_dir`, use mode `0400` or `0600`, and remain available at the same host path for issuance and renewal.
The role mounts it read-only at `/run/secrets/certbot-dns-credentials`.
Put only plugin flags and paths in `certbot_dns_01_args`; keep token and key values in the credentials file.

For example, with the Cloudflare plugin image:

```yaml
certbot_challenge_type: 'dns_01'
certbot_image_repo: 'docker.io/certbot/dns-cloudflare'
certbot_dns_01_credentials_file: '/root/.secrets/certbot/cloudflare.ini'
certbot_dns_01_args:
  - '--dns-cloudflare'
  - '--dns-cloudflare-credentials'
  - '/run/secrets/certbot-dns-credentials'
  - '--dns-cloudflare-propagation-seconds'
  - '60'
```

## Notes

- by default the role does not force an ACME directory URL; certbot uses its own default server selection unless `certbot_server` or `item.server` is set
- HTTP-01 support is infrastructure-level and intended to work with the nginx role’s global HTTP redirect server
- when `nginx_runtime_gid` is available in the play context, the post-success hook adjusts group ownership and permissions under `live/` and `archive/` so nginx can read certbot-managed keys and certificate material before the target service is reloaded
