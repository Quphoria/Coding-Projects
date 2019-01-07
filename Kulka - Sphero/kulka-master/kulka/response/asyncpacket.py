from collections import namedtuple
from itertools import islice


ID_CODE = {
    0x01: 'POWER_NOTIFICATIONS',
    0x02: 'LEVEL_1_DIAGNOSTIC_RESPONSE',
    0x03: 'SENSOR_DATA_STREAMING',
    0x04: 'CONFIG_BLOCK_CONTENTS',
    0x05: 'PRE_SLEEP_WARNING',
    0x06: 'MACRO_MARKERS',
    0x07: 'COLLISION_DETECTED',
    0x08: 'ORBBASIC_PRINT_MESSAGE',
    0x09: 'ORBBASIC_ERROR_MESSAGE_ASCII',
    0x0A: 'ORBBASIC_ERROR_MESSAGE_BINARY',
    0x0B: 'SELF_LEVEL_RESULT',
    0x0C: 'GYRO_AXIS_LIMIT_EXCEEDED',
    0x0D: 'SPHEROS_SOUL_DATA',
    0x0E: 'LEVEL_UP_NOTIFICATION',
    0x0F: 'SHIELD_DAMAGE_NOTIFICATION',
    0x10: 'XP_UPDATE_NOTIFICATION',
    0x11: 'BOOST_UPDATE_NOTIFICATION',
}


AsyncPacket = namedtuple('AsyncPacket', 'id_code data size')


def async_packet_parser(data):
    try:
        if (next(data), next(data)) != (0xFF, 0xFE):
            return

        id_code = next(data)

        if id_code not in ID_CODE:
            return

        dlen_msb = next(data)
        dlen_lsb = next(data)
        dlen = dlen_msb << 8 | dlen_lsb

        data_ = bytearray(islice(data, dlen - 1))
        if dlen - 1 != len(data_):
            return

        chk = (id_code + dlen_msb + dlen_lsb + sum(data_)) & 0xFF ^ 0xFF

        if next(data) != chk:
            return

        return AsyncPacket(ID_CODE[id_code], data_, len(data_) + 6)
    except StopIteration:
        pass
