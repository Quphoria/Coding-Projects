import pytest
from kulka.request.corerequest import CoreRequest


def test_request():
    with pytest.raises(NotImplementedError):
        CoreRequest()
