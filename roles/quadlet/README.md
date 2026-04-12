# Quadlet

Generic role for rendering Podman Quadlet units and managing the generated systemd services.

## Scope

- `.container` units
- `.network` units
- generated systemd service enablement and state management

## Default Hardening Baseline

- `DropCapability=all`
- `NoNewPrivileges=true`
- `ReadOnly=true`
- `ReadOnlyTmpfs=true`
- `CgroupsMode=no-conmon`

This baseline is meant to be loosened selectively per service.

## Important Variables

- `quadlet_unit_dir`
- `quadlet_default_state`
- `quadlet_default_enable`
- `quadlet_default_restart`
- `quadlet_default_cgroups_mode`
- `quadlet_default_drop_capabilities`
- `quadlet_default_no_new_privileges`
- `quadlet_default_read_only`
- `quadlet_default_read_only_tmpfs`
- `quadlet_default_wanted_by`
- `quadlet_networks`
- `quadlet_services`

## Service Features

Container units support:

- unit dependencies such as `Requires`, `Wants`, `After`, and `OnSuccess`
- service controls such as `Restart`, `Type`, `RemainAfterExit`, `TimeoutStartSec`, and `TimeoutStopSec`
- container settings such as `Exec`, `User`, `UserNS`, `Timezone`, `Tmpfs`, `Volume`, `Network`, `PublishPort`, `Secret`, health checks, and arbitrary Podman arguments

Network units support:

- driver selection
- subnet and gateway configuration
- labels, options, and unit-level dependencies

## Notes

- this role is the primitive rendering layer; app or infrastructure roles should prefer passing structured data into it rather than copying templates
- if a higher-level role wants to expose a Quadlet knob while inheriting the primitive default, leave the higher-level variable empty and let the Quadlet layer apply its fallback
