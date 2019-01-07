from kulka.connection import exceptions


def test_connection_lost():
    exception = exceptions.ConnectionLost()
    assert isinstance(exception, exceptions.ConnectionLost)
