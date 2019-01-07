import pytest
from kulka.request import Roll


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x02, 0x30, 0x00, 0x05,
                          0x10, 0x20, 0x30, 0x40, 0x28])
    request = Roll(16, 8240, 64)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, arg3=int, min_num=0, max_num=255)
@pytest.mark.randomize(arg2=int, min_num=0, max_num=65536)
def test_valid_input(arg1, arg2, arg3):
    expected = bytearray([0xFF, 0xFF, 0x2, 0x30, 0x00, 0x05,
                          arg1, (arg2 >> 8), (arg2 & 0xFF), arg3])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = Roll(arg1, arg2, arg3)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, arg3=int, min_num=256)
@pytest.mark.randomize(arg2=int, min_num=65536)
def test_input_above_range(arg1, arg2, arg3):
    request = Roll(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(arg1=int, arg2=int, arg3=int, min_num=-1)
def test_input_below_range(arg1, arg2, arg3):
    request = Roll(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()
