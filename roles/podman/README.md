# Podman

Host baseline for rootful podman usage, with helper entrypoints for optional rootless workflows.

## Scope

- install the distro-maintained podman packages
- create and manage the dedicated `containers` account used for rootful container storage and subordinate ID reservation
- create the rootful Quadlet unit directory
- configure podman-related sysctls
- provide helper task entrypoints for rootless compatibility and user socket activation
- apply the temporary SELinux compatibility module required on affected AlmaLinux 10 hosts

## Core Behavior

- rootful host storage is rooted under `podman_containers_root`, default `/opt/containers`
- system-level Quadlet units are expected under `podman_quadlet_unit_dir`, default `/etc/containers/systemd`
- the `containers` user is created without a home directory
- subordinate UID and GID ranges are assigned to the `containers` user for future namespace-mapping use
- a local SELinux compatibility module is installed only where `container-selinux < 2.241.0` and the AlmaLinux 10 BPF denial is present as a risk

## Important Variables

- `podman_containers_user`
- `podman_containers_root`
- `podman_quadlet_unit_dir`
- `podman_subuid_start`
- `podman_subuid_count`
- `podman_subgid_start`
- `podman_subgid_count`
- `podman_manage_selinux_bpf_compat`

## Notes

- this role is intentionally firewall-agnostic
- `tasks_from: quadlet.yml` can be called directly when only the rootful Quadlet host layout should be reconciled
- rootless helper task files assume the target user is managed elsewhere
- the current model is rootful-first; namespace remapping is intentionally not forced by default
