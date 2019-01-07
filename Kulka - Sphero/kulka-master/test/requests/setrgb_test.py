import pytest
from kulka.request import SetRGB


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x02, 0x20, 0x00, 0x05,
                          0x10, 0x10, 0x10, 0x00, 0xA8])
    request = SetRGB(16, 16, 16, 0)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, arg2=int, arg3=int, arg4=int,
                       min_num=0, max_num=255)
def test_valid_input(arg1, arg2, arg3, arg4):
    expected = bytearray([0xFF, 0xFF, 0x02, 0x20, 0x00, 0x05,
                          arg1, arg2, arg3, arg4])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = SetRGB(arg1, arg2, arg3, arg4)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, arg2=int, arg3=int, min_num=256)
def test_input_above_range(arg1, arg2, arg3):
    request = SetRGB(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(arg1=int, arg2=int, arg3=int, max_num=-1)
def test_input_below_range(arg1, arg2, arg3):
    request = SetRGB(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()
