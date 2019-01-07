import pytest
from kulka.request import SetHeading


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x02, 0x01, 0x00, 0x03, 0x01, 0x2c, 0xCC])
    request = SetHeading(300)
    assert request.tobytes() == expected


@pytest.mark.randomize(heading=int, min_num=0, max_num=65535)
def test_valid_input(heading):
    expected = bytearray([0xFF, 0xFF, 0x02, 0x01, 0x00, 0x03,
                          (heading >> 8) & 0xFF, heading & 0xFF])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = SetHeading(heading)
    assert request.tobytes() == expected


@pytest.mark.randomize(heading=int, min_num=65536)
def test_input_above_range(heading):
    request = SetHeading(heading)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(heading=int, max_num=-1)
def test_input_below_range(heading):
    request = SetHeading(heading)

    with pytest.raises(ValueError):
        request.tobytes()
