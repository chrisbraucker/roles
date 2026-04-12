from ansible.errors import AnsibleFilterError


class FilterModule:
    def filters(self):
        return {
            'default_if_none_or_empty': self.default_if_none_or_empty,
            'strformat': self.strformat,
            'ipv4_to_mac': self.ipv4_to_mac,
        }

    @staticmethod
    def default_if_none_or_empty(value, fallback):
        if value is None or value == '':
            return fallback
        return value

    @staticmethod
    def strformat(value, fmt):
        return fmt % value

    @staticmethod
    def ipv4_to_mac(value, prefix='02:89'):
        try:
            octets = [int(part) for part in str(value).split('.')]
        except ValueError as exc:
            raise AnsibleFilterError(f'invalid IPv4 address for MAC derivation: {value}') from exc

        if len(octets) != 4 or any(octet < 0 or octet > 255 for octet in octets):
            raise AnsibleFilterError(f'invalid IPv4 address for MAC derivation: {value}')

        prefix_octets = str(prefix).split(':')
        if len(prefix_octets) != 2:
            raise AnsibleFilterError(f'invalid MAC prefix for IPv4 derivation: {prefix}')

        try:
            parsed_prefix = [int(part, 16) for part in prefix_octets]
        except ValueError as exc:
            raise AnsibleFilterError(f'invalid MAC prefix for IPv4 derivation: {prefix}') from exc

        return ':'.join(f'{octet:02x}' for octet in parsed_prefix + octets)
