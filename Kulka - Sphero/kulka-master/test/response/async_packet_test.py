import pytest
from kulka.response import parser
from kulka.response.asyncpacket import ID_CODE


def create_async_packet(id_code, data):
    dlen = len(data) + 1
    dlen_msb = dlen >> 8 & 0xFF
    dlen_lsb = dlen & 0xFF
    given = bytearray([0xFF, 0xFE, id_code, dlen_msb, dlen_lsb] + data)
    given.append(sum(given[2:]) & 0xFF ^ 0xFF)
    return given


@pytest.mark.parametrize('id_code', ID_CODE.keys())
@pytest.mark.randomize(data=pytest.nonempty_list_of(int),
                       min_num=0, max_num=255)
def test_truncated_async_packet(id_code, data):
    given = create_async_packet(id_code, data)

    for i in range(len(given) - 1):
        with pytest.raises(ValueError):
            parser(given[:i])


@pytest.mark.parametrize('id_code', ID_CODE.keys())
@pytest.mark.randomize(data=pytest.nonempty_list_of(int),
                       min_num=0, max_num=255)
def test_valid_async_packet(id_code, data):
    response_, _ = parser(create_async_packet(id_code, data))

    assert response_.id_code == ID_CODE[id_code]
    assert response_.data == bytearray(data)


@pytest.mark.parametrize('id_code', ID_CODE.keys())
@pytest.mark.randomize(data=pytest.nonempty_list_of(int),
                       junk=pytest.nonempty_list_of(int),
                       min_num=0, max_num=255)
def test_garbage_before_async(id_code, data, junk):
    given = bytearray(junk) + create_async_packet(id_code, data)
    response_, consumed = parser(given)

    assert consumed == len(junk) + len(data) + 6
    assert response_.id_code == ID_CODE[id_code]
    assert response_.data == bytearray(data)
