# Coder

Deploys the Coder management interface as a rootful Podman
Quadlet-managed service.


## Scope

- creates host directories for Coder runtime configuration and cache data
- renders a root-owned environment file for Coder server settings
- renders a native `.container` Quadlet unit
- enables and starts the generated systemd service


## Important Variables

- `coder_access_url`
- `coder_pg_connection_url`
- `coder_wildcard_access_url`
- `coder_image_repo`
- `coder_image_ref`
- `coder_memory`
- `coder_networks`
- `coder_network_aliases`
- `coder_provisioner_daemons`
- `coder_disable_password_auth`
- `coder_state`
- `coder_enable`


## Defaults

- Coder state is stored in an external PostgreSQL database through
  `coder_pg_connection_url`; the role intentionally rejects an empty value
  instead of relying on Coder's built-in database
- built-in provisioners are disabled by default with
  `coder_provisioner_daemons: 0`, because workspace execution is expected to
  happen on separate worker machines
- TLS is disabled inside Coder by default; nginx or another edge proxy is
  expected to terminate HTTPS
- password authentication remains enabled by default so the initial deployment
  can be bootstrapped before OIDC is added
- the image repository and image ref are separate variables, and the rendered
  systemd description includes the ref
- `coder_memory` is rendered as Quadlet `Memory=` in the `[Container]` section
  only when set
- the container runs as UID/GID `1000:1000` by default
- the Coder cache directory is mounted at `/home/coder/.cache`
- the service name, restart policy, cache mount target, and Quadlet hardening
  settings are intentionally fixed by the role
- the role sets the `coder` DNS name by rendering
  `NetworkAlias=coder` across all attached networks as default


## Nginx

The nginx site should proxy to the Coder container over the shared edge
network, with WebSocket support enabled. A typical host-level site entry uses
`http://systemd-coder:3000` as the upstream and `websocket: true`.

If `coder_wildcard_access_url` is set for workspace applications, DNS,
certificate issuance, and nginx `server_name` entries must also cover that
wildcard name.


## PostgreSQL

The `postgres` role can create a dedicated database and owner role for Coder:

```yaml
postgres_databases:
  - name: 'coder'
    owner: 'coder'
    password: '{{ coder_postgres_password }}'

coder_pg_connection_url: >-
  postgres://coder:{{ coder_postgres_password | urlencode }}@systemd-postgres/coder?sslmode=disable
```


## Notes

- this role does not install Podman or prepare the Quadlet unit directory; apply
  the `podman` role first
- this role intentionally renders a native Quadlet template instead of routing
  through the generic `quadlet` role
- OIDC/ZITADEL integration is intentionally left out for now and should be added
  as a separate step
