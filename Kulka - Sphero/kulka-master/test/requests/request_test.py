import pytest
from kulka.request.request import Request


def test_instiate_request():
    with pytest.raises(NotImplementedError):
        Request()
