# Postgres

Quadlet-managed PostgreSQL role for single-host deployments with persistent
host storage and one-time superuser bootstrap.


## Core Behavior

- stores PostgreSQL data on the host via a bind mount
- uses `postgres_superuser_password` when it is supplied explicitly
- otherwise generates a random superuser password on the control host during bootstrap
- archives the generated bootstrap password in a local plain-text file for later operator import
- creates a Podman secret on the target host from the effective password
- passes the secret into the PostgreSQL container through `POSTGRES_PASSWORD_FILE`


## Important Variables

- `postgres_base_dir`
- `postgres_data_dir`
- `postgres_image`
- `postgres_service_name`
- `postgres_publish_ports`
- `postgres_networks`
- `postgres_superuser_name`
- `postgres_database_name`
- `postgres_secret_name`
- `postgres_secret_target`
- `postgres_secret_driver`
- `postgres_superuser_password`
- `postgres_local_password_dir`
- `postgres_local_password_file`


## Notes

- this first-cut role does not manage TLS
- if the target host already has the Podman secret, set
  `postgres_superuser_password` explicitly so reruns do not depend on the local
  bootstrap archive file
- secret handling lives in `tasks/secret.yml`, so it can be called directly for
  rotation with `tasks_from: secret.yml` and
  `postgres_secret_force_recreate: true`
- the default Podman secret driver is `file`; this keeps the container runtime
  cleaner than a manual bind mount, but it is not a replacement for a dedicated
  secret manager
