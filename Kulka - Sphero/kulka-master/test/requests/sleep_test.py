import pytest
from kulka.request import Sleep


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x00, 0x22, 0x00, 0x06,
                          0x04, 0xD2, 0x38, 0x1E, 0xD2, 0xD9])
    request = Sleep(1234, 56, 7890)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg2=int, min_num=0, max_num=255)
@pytest.mark.randomize(arg1=int, arg3=int, min_num=0, max_num=65536)
def test_valid_input(arg1, arg2, arg3):
    expected = bytearray([0xFF, 0xFF, 0x00, 0x22, 0x00, 0x06,
                          (arg1 >> 8), (arg1 & 0xFF), arg2,
                          (arg3 >> 8), (arg3 & 0xFF)])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = Sleep(arg1, arg2, arg3)
    assert request.tobytes() == expected


@pytest.mark.randomize(arg1=int, arg3=int, min_num=65536)
@pytest.mark.randomize(arg2=int, min_num=256)
def test_input_above_range(arg1, arg2, arg3):
    request = Sleep(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(arg1=int, arg2=int, arg3=int, min_num=-1)
def test_input_below_range(arg1, arg2, arg3):
    request = Sleep(arg1, arg2, arg3)

    with pytest.raises(ValueError):
        request.tobytes()
