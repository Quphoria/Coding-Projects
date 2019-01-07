from kulka.connection import exceptions


def test_connection_failed():
    exception = exceptions.ConnectionFailed()
    assert isinstance(exception, exceptions.ConnectionFailed)
