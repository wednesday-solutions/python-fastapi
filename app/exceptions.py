from __future__ import annotations


class ExternalServiceException(Exception):
    pass


class NoUserFoundException(Exception):
    pass


class EmailAlreadyExistException(Exception):
    pass


class MobileAlreadyExistException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class CentryTestException(Exception):
    pass


class DatabaseConnectionException(Exception):
    pass


class RedisUrlNotFoundException(Exception):
    pass
