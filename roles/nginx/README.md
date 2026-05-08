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
- runs the container as the configured UID/GID and adds `NET_BIND_SERVICE` so
  nginx can still bind `80` and `443`


## Important Variables

- `nginx_image_repo`
- `nginx_image_ref`
- `nginx_memory`
- `nginx_service_name`
- `nginx_quadlet_unit_dir`
- `nginx_container_uid`
- `nginx_container_gid`
- `nginx_networks`
- `nginx_network_aliases`
- `nginx_global_https_redirect`
- `nginx_global_https_redirect_http_port`
- `nginx_mount_letsencrypt`
- `nginx_letsencrypt_dir`
- `nginx_certbot_http_01_enabled`
- `nginx_certbot_http_01_webroot`
- `nginx_limit_req_zones`
- `nginx_limit_conn_zones`
- `nginx_http_site_use_default_limits`
- `nginx_http_site_default_limit_req`
- `nginx_http_site_default_limit_conn`
- `nginx_global_https_redirect_limit_req`
- `nginx_global_https_redirect_limit_conn`


## Quadlet Behavior

The role renders its own native `.container` unit and does not route nginx
through the generic `quadlet` role. Network units are not created by this role;
create them explicitly in the site playbook and pass the desired attachments
through `nginx_networks`.

The container name, restart policy, systemd timeouts, health check, published
ports, environment, hardening settings, and `NET_BIND_SERVICE` capability are
intentionally fixed by the role until the deployment needs a concrete reason to
expose them.

`nginx_memory` is rendered as Quadlet `Memory=` in the `[Container]` section
only when set.


## HTTP Site Behavior

- `tls_certificate_name` derives `fullchain.pem`, `privkey.pem`, and `chain.pem` paths under `/etc/letsencrypt/live/<name>/`
- per-site `hsts: true` enables HSTS using `nginx_http_site_hsts_header_value`
- by default, HTTP sites inherit server-level request-rate and connection limits from `nginx_http_site_default_limit_req` and `nginx_http_site_default_limit_conn`
- set `use_default_limits: false` on a site to opt out, or define `limit_req` / `limit_conn` explicitly per site
- the global HTTP redirect server uses `nginx_global_https_redirect_limit_req` and `nginx_global_https_redirect_limit_conn`, which default to the same baseline as normal HTTP sites
- server-level `limit_req` entries support:
  - `zone`
  - optional `burst`
  - optional `delay`
  - optional `nodelay`
- server-level `limit_conn` entries support:
  - `zone`
  - `count`
- per-location proxy controls support:
  - `proxy_buffering`
  - `proxy_request_buffering`
  - `proxy_send_timeout`
  - `proxy_read_timeout`
  - `gzip_off`
- per-location gRPC controls support:
  - `grpc_pass`
  - optional `grpc_set_headers`
  - optional `grpc_connect_timeout`
  - optional `grpc_send_timeout`
  - optional `grpc_read_timeout`
- per-location `limit_req` and `limit_conn` use the same option shapes as the server-level directives above


## Default Limit Baseline

The role now renders global zones and applies them to HTTP sites by default:

- request rate zone `perip_req`
  - key: `$binary_remote_addr`
  - size: `10m`
  - rate: `15r/s`
- connection zone `perip_conn`
  - key: `$binary_remote_addr`
  - size: `10m`
- default per-site request limiting:
  - `limit_req zone=perip_req burst=30`
- default per-site connection limiting:
  - `limit_conn perip_conn 20`

These are conservative ingress-hardening defaults for authenticated services, not a substitute for application authentication or a WAF.


## Global Limit Configuration

The following variables control the `http`-scope limit configuration rendered into `nginx.conf`, they closely mirror the nginx [http_limit_req](https://nginx.org/en/docs/http/ngx_http_limit_req_module.html) and [http_limit_conn](https://nginx.org/en/docs/http/ngx_http_limit_conn_module.html) modules:

- `nginx_limit_req_status`
  - HTTP status returned when a request rate limit is exceeded
- `nginx_limit_req_log_level`
  - log level used when request rate limiting triggers
- `nginx_limit_req_zones`
  - list of request-rate zone objects with:
    - `name`
    - `key`
    - `size`
    - `rate`
    - optional `sync`
- `nginx_limit_conn_status`
  - HTTP status returned when a connection limit is exceeded
- `nginx_limit_conn_log_level`
  - log level used when connection limiting triggers
- `nginx_limit_conn_zones`
  - list of connection-limit zone objects with:
    - `name`
    - `key`
    - `size`

These zones are then referenced by the server-level and location-level `limit_req` and `limit_conn` directives documented above.


## Notes

- the global HTTP redirect server also hosts the certbot HTTP-01 challenge path so HTTPS-only vhosts do not create a bootstrap problem
- this role does not install Podman or prepare the Quadlet unit directory; apply
  the `podman` role first
