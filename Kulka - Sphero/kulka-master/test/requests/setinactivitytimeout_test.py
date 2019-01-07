import pytest
from kulka.request import SetInactivityTimeout


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x00, 0x25, 0x00, 0x03, 0x04, 0xD2, 0x01])
    request = SetInactivityTimeout(1234)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, min_num=0, max_num=65536)
def test_valid_input(arg1):
    expected = bytearray([0xFF, 0xFF, 0x00, 0x25, 0x00, 0x03,
                          (arg1 >> 8), (arg1 & 0xFF)])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = SetInactivityTimeout(arg1)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, min_num=65536)
def test_input_above_range(arg1):
    request = SetInactivityTimeout(arg1)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(arg1=int, max_num=-1)
def test_input_below_range(arg1):
    request = SetInactivityTimeout(arg1)

    with pytest.raises(ValueError):
        request.tobytes()
