class DNSRecordAlreadyExistsError(Exception):
    pass


class DNSRecordNotFoundError(Exception):
    pass


class IdentifierTokenAlreadyExistsError(Exception):
    pass


class IdentifierTokenNotFoundError(Exception):
    pass


class SecretTokenIncorrectError(Exception):
    pass
