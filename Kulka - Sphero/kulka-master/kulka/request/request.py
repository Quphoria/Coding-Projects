import struct


class Request(object):

    DID = None
    CID = None
    FMT = ''

    def __new__(cls, *_, **__):
        if cls.DID is None or cls.CID is None:
            raise NotImplementedError()

        return super(Request, cls).__new__(cls)

    def __init__(self, *args):
        self.answer = True
        self.sequence = 0
        self._data = args

    @classmethod
    def async(cls, *args):
        obj = cls(*args)
        obj.answer = False
        return obj

    def _sop(self):
        if self.answer:
            return bytearray([0xFF, 0xFF])
        else:
            return bytearray([0xFF, 0xFE])

    def tobytes(self):
        packet = bytearray([self.DID, self.CID])

        if self.answer:
            packet.append(self.sequence)

        if self._data:
            try:
                data = struct.pack(self.FMT, *self._data)
            except struct.error as exception:
                raise ValueError(str(exception))

            packet.append(len(data) + 1)
            packet.extend(data)
        else:
            packet.append(1)

        packet.append((sum(packet) & 0xFF) ^ 0xFF)

        return bytes(self._sop() + packet)
