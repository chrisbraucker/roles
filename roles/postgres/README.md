# Postgres

Quadlet-managed PostgreSQL role for single-host deployments with persistent
host storage and one-time superuser bootstrap.


## Core Behavior

- stores PostgreSQL data on the host via a bind mount
- checks whether the data directory is already initialized via `PG_VERSION`
- if not initialized, runs a one-shot bootstrap container using the official PostgreSQL image
- mounts a managed init script into `/docker-entrypoint-initdb.d` during bootstrap only
- waits on a host-side completion marker written by that init script instead of parsing container logs
- uses `postgres_superuser_password` when it is supplied explicitly
- otherwise generates a random superuser password on the control host during bootstrap
- archives the generated bootstrap password in a local plain-text file for later operator import
- creates a Podman secret on the target host only for first initialization
- passes the secret into the bootstrap container through `POSTGRES_PASSWORD_FILE`
- removes the bootstrap Podman secret from the target host after initialization has completed
- deploys the long-lived Quadlet service only after bootstrap and without any secret mount


## Important Variables

- `postgres_base_dir`
- `postgres_data_dir`
- `postgres_bootstrap_dir`
- `postgres_bootstrap_init_dir`
- `postgres_bootstrap_marker_file`
- `postgres_quadlet_unit_dir`
- `postgres_container_user`
- `postgres_container_group`
- `postgres_version`
- `postgres_image_repo`
- `postgres_image_ref`
- `postgres_service_name`
- `postgres_networks`
- `postgres_superuser_name`
- `postgres_secret_name`
- `postgres_secret_target`
- `postgres_secret_driver`
- `postgres_bootstrap_container_name`
- `postgres_bootstrap_marker_script_name`
- `postgres_bootstrap_wait_retries`
- `postgres_bootstrap_wait_delay`
- `postgres_superuser_password`
- `postgres_local_password_dir`
- `postgres_local_password_file`


## Notes

- this role does not manage TLS
- this role does not install Podman or prepare the Quadlet unit directory; apply
  the `podman` role first
- once `{{ postgres_data_dir }}/{{ postgres_version }}/docker/PG_VERSION`
  exists, the role no longer mounts or requires the bootstrap Podman secret on
  ordinary reruns
- bootstrap uses the upstream image initialization flow intentionally; the role
  does not reimplement `initdb`
- bootstrap completion is signaled by a managed init script writing a marker
  file under `postgres_bootstrap_dir`, not by parsing container logs
- password rotation is intentionally out of scope for this role and should be
  handled at the SQL level rather than by replacing the bootstrap secret
- the default Podman secret driver is `file`; this keeps the container runtime
  cleaner than a manual bind mount, but it is not a replacement for a dedicated
  secret manager
- this role renders its own native Quadlet container unit and does not manage
  Quadlet network units; pass existing network attachments through
  `postgres_networks`
