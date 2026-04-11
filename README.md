# Ansible Roles

Ansible roles for some light infrastructure management and workload deployment via podman's quadlet feature.\
Efficient, boring, and just works.

## Roles

### Bastion

Hardens hosts that are exposed to the elements with firewall, fail2ban and others.


### Common

Configures defaults for debian and almalinux-based distros.

Notable options:
- `common_ssh_authorized_keys`: exclusive SSH keys for the management user when non-empty
- `common_journald_manage`: manages a `journald.conf.d` drop-in when enabled
- `common_journald_storage`: journald storage mode, for example `volatile` for memory-only host logs

### Nginx

Deploys nginx as a Quadlet-managed reverse proxy and renders `nginx.conf` plus structured HTTP and stream site definitions into a mounted host config tree.

Entry points:
- `main`: deploys nginx core, directories, base config, and the Quadlet-managed container
- `http_site`: renders HTTP site definitions, include snippets, and HTTP snippets
- `stream_site`: renders stream proxy definitions and stream snippets

Core options:
- `nginx_global_https_redirect`: renders a catch-all HTTP server that redirects all requests to HTTPS
- `nginx_global_https_redirect_http_port`: HTTP listen port for that redirect server, default `80`
- `nginx_ssl_session_cache`: global TLS session cache policy, default `shared:SSL:10m`
- `nginx_ssl_session_timeout`: global TLS session reuse timeout, default `1h`
- `nginx_ssl_stapling_enabled`: feature-gates OCSP stapling and requires resolver configuration plus trusted chain paths on HTTPS sites

HTTP site behavior:
- per-site `hsts: true` enables HSTS; the header value defaults to `nginx_http_site_hsts_header_value`
- per-site `tls_certificate_name` derives Let’s Encrypt paths under `/etc/letsencrypt/live/<name>/` when `nginx_mount_letsencrypt` is enabled
- per-location proxy controls support `proxy_buffering`, `proxy_request_buffering`, `proxy_send_timeout`, and `proxy_read_timeout`


### Podman

Ensures presence of the latest distro-maintained podman version on the host and configures sysctls for low-friction, rootful container usage.
Additionally provides helpers to enable rootless container execution beyond session lifecycle via linger.


### Quadlet

Generic role to deploy containerized services via Podman Quadlet as systemD-managed services.
Provides support for containers and networks, which can be consumed as lightweight playbook-driven instructions or by other roles if more configuration is needed.
