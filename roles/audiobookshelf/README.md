# Audiobookshelf

Deploys Audiobookshelf as a rootful Podman Quadlet-managed service.


## Scope

- creates the Audiobookshelf host storage directories
- renders a native `.container` Quadlet unit
- enables and starts the generated systemd service


## Important Variables

- `audiobookshelf_root`
- `audiobookshelf_quadlet_unit_dir`
- `audiobookshelf_image_repo`
- `audiobookshelf_image_ref`
- `audiobookshelf_container_uid`
- `audiobookshelf_container_gid`
- `audiobookshelf_port`
- `audiobookshelf_networks`
- `audiobookshelf_state`
- `audiobookshelf_enabled`


## Defaults

- storage is rooted under `podman_containers_root` when that variable is
  available, otherwise `/opt/containers`
- Quadlet units are rendered under `podman_quadlet_unit_dir` when that variable
  is available, otherwise `/etc/containers/systemd`
- the default container name and network alias are both `audiobookshelf`
- the image repository and image ref are separate variables, and the rendered
  systemd description includes the ref
- no `PORT` environment variable is rendered unless `audiobookshelf_port` is set
- the container runs as UID/GID `150:150` by default, and managed host
  directories are owned by that identity so writable bind mounts do not require
  a root process inside the container
- the service name, container name, restart policy, storage subdirectories, and
  Quadlet hardening settings are intentionally fixed by the role


## Notes

- this role does not install Podman or prepare the Quadlet unit directory; apply
  the `podman` role first
- this role intentionally renders a native Quadlet template instead of routing
  through the generic `quadlet` role
