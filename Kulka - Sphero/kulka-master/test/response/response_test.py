import pytest
from kulka.response import parser
from kulka.response.responsepacket import MRSP


def create_response(mrsp, seq, data):
    given = bytearray([0xFF, 0xFF, mrsp, seq, len(data) + 1] + data)
    given.append(sum(given[2:]) & 0xFF ^ 0xFF)
    return given


@pytest.mark.parametrize('mrsp', MRSP.keys())
@pytest.mark.randomize(seq=int, data=pytest.nonempty_list_of(int),
                       min_num=0, max_num=255)
def test_truncated_response(mrsp, seq, data):
    given = create_response(mrsp, seq, data)

    for i in range(len(given) - 1):
        with pytest.raises(ValueError):
            parser(given[:i])


@pytest.mark.parametrize('mrsp', MRSP.keys())
@pytest.mark.randomize(seq=int, data=pytest.nonempty_list_of(int),
                       min_num=0, max_num=255)
def test_valid_response(mrsp, seq, data):
    response_, _ = parser(create_response(mrsp, seq, data))

    assert response_.mrsp == MRSP[mrsp]
    assert response_.seq == seq
    assert response_.data == bytearray(data)


@pytest.mark.parametrize('mrsp', MRSP.keys())
@pytest.mark.randomize(seq=int, data=pytest.nonempty_list_of(int),
                       junk=pytest.nonempty_list_of(int), min_num=0,
                       max_num=255)
def test_garbage_before_response(mrsp, seq, data, junk):
    given = bytearray(junk) + create_response(mrsp, seq, data)
    response_, consumed = parser(given)

    assert consumed == len(junk) + len(data) + 6
    assert response_.mrsp == MRSP[mrsp]
    assert response_.seq == seq
    assert response_.data == bytearray(data)
