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
  create the first instance, and generate IAM owner and login-client PATs
- runs the steady-state ZITADEL service through Quadlet with `zitadel start`
- deploys the self-hosted `zitadel-login` UI by default and wires it to a
  login-client PAT written by ZITADEL during first-instance setup
- expects PostgreSQL connectivity and credentials to be supplied explicitly
- assumes TLS is terminated upstream, typically by nginx, using ZITADEL TLS mode
  `external`


## Important Variables

- `zitadel_image_repo`
- `zitadel_image_ref`
- `zitadel_memory`
- `zitadel_quadlet_unit_dir`
- `zitadel_container_user`
- `zitadel_container_group`
- `zitadel_service_name`
- `zitadel_service_dependencies`
- `zitadel_networks`
- `zitadel_network_aliases`
- `zitadel_state`
- `zitadel_enable`
- `zitadel_restart`
- `zitadel_timeout_start`
- `zitadel_timeout_stop`
- `zitadel_init_timeout`
- `zitadel_setup_timeout`
- `zitadel_setup_revision`
- `zitadel_log_level`
- `zitadel_listen_port`
- `zitadel_external_domain`
- `zitadel_external_port`
- `zitadel_external_secure`
- `zitadel_tls_enabled`
- `zitadel_tls_mode`
- `zitadel_database_host`
- `zitadel_database_port`
- `zitadel_database_name`
- `zitadel_database_user_username`
- `zitadel_database_user_password`
- `zitadel_database_admin_username`
- `zitadel_database_admin_password`
- `zitadel_firstinstance_org_human_username`
- `zitadel_firstinstance_org_human_password`
- `zitadel_firstinstance_machine_pat_container_path`
- `zitadel_firstinstance_machine_username`
- `zitadel_firstinstance_machine_name`
- `zitadel_firstinstance_machine_pat_expiration_date`
- `zitadel_firstinstance_trusted_domains`
- `zitadel_masterkey`
- `zitadel_login_enabled`
- `zitadel_login_image_repo`
- `zitadel_login_image_ref`
- `zitadel_login_memory`
- `zitadel_login_service_name`
- `zitadel_login_networks`
- `zitadel_login_network_aliases`
- `zitadel_login_state`
- `zitadel_login_enable`
- `zitadel_login_restart`
- `zitadel_login_timeout_start`
- `zitadel_login_timeout_stop`
- `zitadel_login_base_path`
- `zitadel_login_base_uri`
- `zitadel_login_api_url`
- `zitadel_login_custom_request_headers`


## Notes

- this first-cut role does not manage internal TLS between ZITADEL and
  PostgreSQL
- the `podman` role must run before this role so Podman, the Quadlet generator,
  and `zitadel_quadlet_unit_dir` already exist
- `zitadel_service_dependencies` can be used to add explicit systemd ordering
  and requirement edges such as `postgres.service`
- this role does not manage network units; `zitadel_networks` and
  `zitadel_login_networks` attach containers to existing Podman networks
- `zitadel_memory` and `zitadel_login_memory` render Quadlet `Memory=` in the
  respective `[Container]` sections only when set
- the role stores database credentials and first-instance credentials in
  root-only host files rendered from Ansible variables
- the first-instance IAM owner PAT is written to
  `zitadel_firstinstance_machine_pat_container_path`; store it outside the
  deployment host after the initial setup
- the Podman secret for the masterkey is only created when absent; rotation is
  intentionally left out of this first version
- the role is split into `tasks/init.yml`, `tasks/setup.yml`, `tasks/login.yml`,
  and `tasks/main.yml`
- `init` is treated as a one-time lifecycle step and writes
  `zitadel_init_marker_file`
- `setup` writes a revision-scoped marker file derived from
  `zitadel_setup_revision`, which defaults to the full ZITADEL image reference
- login UI deployment lives in `tasks/login.yml` and is included from `main.yml`
  behind `zitadel_login_enabled`, which defaults to `true`
- the role sets the `zitadel` and `zitadel-login` DNS name by rendering
  `NetworkAlias=$NAME` across all attached networks as default
