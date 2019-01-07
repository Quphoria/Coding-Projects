import pytest
from kulka.request import SetBackLed


def test_example_input():
    expected = bytearray([0xFF, 0xFF, 0x02, 0x21, 0x00, 0x02, 0x10, 0xCA])
    request = SetBackLed(16)
    assert request.tobytes() == expected


@pytest.mark.randomize(bright=int, min_num=0, max_num=255)
def test_valid_input(bright):
    expected = bytearray([0xFF, 0xFF, 0x02, 0x21, 0x00, 0x02, bright])
    expected.append((sum(expected[2:]) & 0xFF) ^ 0xFF)

    request = SetBackLed(bright)
    assert request.tobytes() == expected


@pytest.mark.randomize(bright=int, min_num=256)
def test_input_above_range(bright):
    request = SetBackLed(bright)

    with pytest.raises(ValueError):
        request.tobytes()


@pytest.mark.randomize(bright=int, max_num=-1)
def test_input_below_range(bright):
    request = SetBackLed(bright)

    with pytest.raises(ValueError):
        request.tobytes()
