# Certbot

Containerized certbot role built on Quadlet and systemd timers.

## Entry Points

- `main`
  - deploys the renewal container, post-success reload hook, and timer
- `certificates`
  - issues or updates certificate lineages from structured certificate objects
- `http_01`
  - prepares the shared ACME webroot for HTTP-01 challenges

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

## Notes

- by default the role does not force an ACME directory URL; certbot uses its own default server selection unless `certbot_server` or `item.server` is set
- HTTP-01 support is infrastructure-level and intended to work with the nginx role’s global HTTP redirect server
- when `nginx_runtime_gid` is available in the play context, the post-success hook adjusts group ownership and permissions under `live/` and `archive/` so nginx can read certbot-managed keys and certificate material before the target service is reloaded
