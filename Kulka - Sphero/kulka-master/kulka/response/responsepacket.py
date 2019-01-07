from collections import namedtuple
from itertools import islice


MRSP = {
    0x00: 'OK',
    0x01: 'EGEN',
    0x02: 'ECHKSUM',
    0x03: 'EFRAG',
    0x04: 'EBAD_CMD',
    0x05: 'EUNSUPP',
    0x06: 'EBAD_MSG',
    0x07: 'EPARAM',
    0x08: 'EEXEC',
    0x09: 'EBAD_DID',
    0x0A: 'MEM_BUSY',
    0x0B: 'BAD_PASSWORD',
    0x31: 'POWER_NOGOOD',
    0x32: 'PAGE_ILLEGAL',
    0x33: 'FLASH_FAIL',
    0x34: 'MA_CORRUPT',
    0x35: 'MSG_TIMEOUT',
}


ResponsePacket = namedtuple('ResponsePacket', 'mrsp seq data size')


def response_packet_parser(input_iter):
    try:
        if (next(input_iter), next(input_iter)) != (0xFF, 0xFF):
            return

        mrsp = next(input_iter)
        if mrsp not in MRSP:
            return

        seq = next(input_iter)
        dlen = next(input_iter)
        data_ = bytearray(islice(input_iter, dlen - 1))

        if dlen - 1 != len(data_):
            return

        chk = (mrsp + seq + dlen + sum(data_)) & 0xFF ^ 0xFF

        if chk != next(input_iter):
            return

        return ResponsePacket(MRSP[mrsp], seq, data_, len(data_) + 6)
    except StopIteration:
        pass
