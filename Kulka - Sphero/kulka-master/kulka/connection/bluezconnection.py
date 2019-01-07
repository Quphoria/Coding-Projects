from kulka.connection import exceptions
from kulka.connection.baseconnection import BaseConnection
from kulka.core.logger import debuglog
import bluetooth
import errno
import re
import time


ERR_PATTERN = re.compile(r"\((\d+), '(.+)'\)")


@debuglog
def errstr_parse(errstr):
    match = ERR_PATTERN.match(str(errstr))

    if match is not None:
        return int(match.group(1))

    return 0


class Connection(BaseConnection):

    @classmethod
    @debuglog
    def connect(cls, addr, port=1):
        retries = 50

        while retries > 0:
            try:
                sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                sock.connect((addr, port))
                return cls(sock)
            except bluetooth.btcommon.BluetoothError as error:
                sock.close()
                time.sleep(1)

                if errstr_parse(error) == errno.EHOSTDOWN:
                    retries -= 1

        raise exceptions.ConnectionFailed()
