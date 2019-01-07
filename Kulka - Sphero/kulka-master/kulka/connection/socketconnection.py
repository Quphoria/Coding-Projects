from kulka.connection.baseconnection import BaseConnection
from kulka.connection import exceptions
from kulka.core.logger import debuglog
import errno
import socket
import time


class Connection(BaseConnection):

    @classmethod
    @debuglog
    def connect(cls, addr, port=1):
        retries = 50

        while retries > 0:
            try:
                sock = socket.socket(socket.AF_BLUETOOTH,
                                     socket.SOCK_STREAM,
                                     socket.BTPROTO_RFCOMM)
                sock.connect((addr, port))
                return cls(sock)
            except socket.error as error:
                sock.close()
                time.sleep(1)

                if error.errno == errno.EHOSTDOWN:
                    retries -= 1

        raise exceptions.ConnectionFailed()
