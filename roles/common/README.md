# Common

Baseline host configuration for Debian- and AlmaLinux-based systems.

## Scope

- SSH key management for the primary management user
- host journald baseline
- distro-specific baseline tasks that are not tied to podman, ingress, or firewall policy

## Notable Options

- `common_ssh_authorized_keys`
  - when non-empty, manages the management user's `authorized_keys` file exclusively
  - when empty, leaves the file untouched
- `common_journald_manage`
  - enables management of a `journald.conf.d` drop-in
- `common_journald_storage`
  - sets journald storage mode, for example `volatile`

## Notes

- journald configuration is host policy and belongs here rather than in `podman`
- firewall package management and firewalld-specific behavior live in the `firewall` role
