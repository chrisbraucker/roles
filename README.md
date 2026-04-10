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


### Podman

Ensures presence of the latest distro-maintained podman version on the host and configures sysctls for low-friction, rootful container usage.
Additionally provides helpers to enable rootless container execution beyond session lifecycle via linger.


### Quadlet

Generic role to deploy containerized services via Podman Quadlet as systemD-managed services.
Provides support for containers and networks, which can be consumed as lightweight playbook-driven instructions or by other roles if more configuration is needed.
