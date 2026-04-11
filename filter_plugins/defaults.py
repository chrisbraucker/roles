class FilterModule:
    def filters(self):
        return {
            'default_if_none_or_empty': self.default_if_none_or_empty,
        }

    @staticmethod
    def default_if_none_or_empty(value, fallback):
        if value is None or value == '':
            return fallback
        return value
