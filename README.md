# Ansible Roles

Ansible roles for some light infrastructure management and workload deployment via podman's quadlet feature.\
Efficient, boring, and just works.

## Roles

### Bastion

Hardens hosts that are exposed to the elements with firewall, fail2ban and others.

[Bastion README](roles/bastion/README.md)


### Common

Configures defaults for debian and almalinux-based distros.

[Common README](roles/common/README.md)


### Firewall

Installs and manages the host firewall baseline via firewalld.

[Firewall README](roles/firewall/README.md)


### Certbot

Deploys certbot renewal as a Quadlet-managed oneshot container plus a systemd timer.

[Certbot README](roles/certbot/README.md)


### Nginx

Deploys nginx as a Quadlet-managed reverse proxy and renders `nginx.conf` plus structured HTTP and stream site definitions into a mounted host config tree.

[Nginx README](roles/nginx/README.md)


### Podman

Ensures presence of the latest distro-maintained podman version on the host and configures sysctls for low-friction, rootful container usage.
Additionally provides helpers to enable rootless container execution beyond session lifecycle via linger.

[Podman README](roles/podman/README.md)


### Quadlet

Generic role to deploy containerized services via Podman Quadlet as systemD-managed services.
Provides support for containers and networks, which can be consumed as lightweight playbook-driven instructions or by other roles if more configuration is needed.

[Quadlet README](roles/quadlet/README.md)
