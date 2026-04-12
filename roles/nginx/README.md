# Nginx

Quadlet-managed nginx reverse proxy role with structured HTTP and stream site rendering.

## Entry Points

- `main`
  - deploys nginx core, host directories, base config, and the Quadlet-managed container
- `http_site`
  - renders HTTP sites and related snippets
- `stream_site`
  - renders stream proxy definitions and related snippets

## Core Behavior

- mounts only `nginx.conf` plus managed config subdirectories into `/etc/nginx`
- can consume certbot-managed certificates directly from the mounted Let's Encrypt tree
- can serve the certbot HTTP-01 webroot from the global HTTP redirect server
- runs the container as the configured runtime UID/GID and adds `NET_BIND_SERVICE` so nginx can still bind `80` and `443`

## Important Variables

- `nginx_image`
- `nginx_service_name`
- `nginx_container_user`
- `nginx_publish_ports`
- `nginx_networks`
- `nginx_global_https_redirect`
- `nginx_global_https_redirect_http_port`
- `nginx_mount_letsencrypt`
- `nginx_letsencrypt_dir`
- `nginx_certbot_http_01_enabled`
- `nginx_certbot_http_01_webroot`
- `nginx_static_edge_ip_enabled`
- `nginx_static_edge_ip`
- `nginx_static_edge_mac`
- `nginx_static_edge_mac_prefix`

## Static Edge IP Behavior

When `nginx_static_edge_ip_enabled` is set:

- the first network in `nginx_networks` is treated as the ingress-facing edge attachment
- the role assigns nginx a stable IP on that network
- the role also assigns a stable MAC to avoid stale host neighbor-cache entries after container recreation

If `nginx_static_edge_mac` is unset, the role derives a deterministic locally administered MAC from the static IP using `nginx_static_edge_mac_prefix`.

Default derivation example:

- `10.89.0.2` -> `02:89:0a:59:00:02`

This avoids manual MAC bookkeeping while keeping the L2 identity stable across recreations.

## HTTP Site Behavior

- `tls_certificate_name` derives `fullchain.pem`, `privkey.pem`, and `chain.pem` paths under `/etc/letsencrypt/live/<name>/`
- per-site `hsts: true` enables HSTS using `nginx_http_site_hsts_header_value`
- per-location proxy controls support:
  - `proxy_buffering`
  - `proxy_request_buffering`
  - `proxy_send_timeout`
  - `proxy_read_timeout`
  - `gzip_off`

## Notes

- the global HTTP redirect server also hosts the certbot HTTP-01 challenge path so HTTPS-only vhosts do not create a bootstrap problem
- if you rely on static ingress IP forwarding from the host, prefer the role’s stable-MAC behavior over manual neighbor-cache flushing
