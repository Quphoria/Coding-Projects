import pytest
from kulka.request.kulkarequest import KulkaRequest


def test_instiate_request():
    with pytest.raises(NotImplementedError):
        KulkaRequest()
