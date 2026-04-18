# Zitadel

Quadlet-managed ZITADEL role for a first-cut self-hosted deployment backed by
PostgreSQL.


## Core Behavior

- renders root-only ZITADEL runtime, secret, and initialization-step
  configuration files on the host
- creates a Podman secret for the ZITADEL masterkey
- runs `zitadel init` synchronously through `podman run` to provision the
  database and bootstrap schemas
- runs `zitadel setup` synchronously through `podman run` to apply setup,
  create the first instance, and generate the login-client PAT
- runs the steady-state ZITADEL service through Quadlet with `zitadel start`
- deploys the self-hosted `zitadel-login` UI by default and wires it to a
  login-client PAT written by ZITADEL during first-instance setup
- expects PostgreSQL connectivity and credentials to be supplied explicitly
- assumes TLS is terminated upstream, typically by nginx, using ZITADEL TLS mode
  `external`


## Important Variables

- `zitadel_image`
- `zitadel_service_name`
- `zitadel_publish_ports`
- `zitadel_networks`
- `zitadel_init_timeout`
- `zitadel_setup_timeout`
- `zitadel_setup_revision`
- `zitadel_external_domain`
- `zitadel_external_port`
- `zitadel_external_secure`
- `zitadel_database_host`
- `zitadel_database_port`
- `zitadel_database_name`
- `zitadel_database_user_username`
- `zitadel_database_user_password`
- `zitadel_database_admin_username`
- `zitadel_database_admin_password`
- `zitadel_firstinstance_org_human_username`
- `zitadel_firstinstance_org_human_password`
- `zitadel_masterkey`
- `zitadel_login_enabled`
- `zitadel_login_image`
- `zitadel_login_service_name`
- `zitadel_login_base_path`
- `zitadel_login_base_uri`
- `zitadel_login_api_url`


## Notes

- this first-cut role does not manage internal TLS between ZITADEL and
  PostgreSQL
- the role stores database credentials and first-instance credentials in
  root-only host files rendered from Ansible variables
- the Podman secret for the masterkey is only created when absent; rotation is
  intentionally left out of this first version
- the role is split into `tasks/init.yml`, `tasks/setup.yml`, `tasks/login.yml`,
  and `tasks/main.yml`
- `init` is treated as a one-time lifecycle step and writes
  `zitadel_init_marker_file`
- `setup` writes a revision-scoped marker file derived from
  `zitadel_setup_revision`, which defaults to `zitadel_image`
- login UI deployment lives in `tasks/login.yml` and is included from `main.yml`
  behind `zitadel_login_enabled`, which defaults to `true`
