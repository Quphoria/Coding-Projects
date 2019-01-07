try:
    import bluetooth
    from kulka.connection.bluezconnection import Connection
except ImportError:
    import socket

    if not hasattr(socket, 'AF_BLUETOOTH'):
        raise

    from kulka.connection.socketconnection import Connection

__all__ = ['Connection']
