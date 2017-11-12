""" Тесты для JIMMessage """
import pytest
import time

from JIM import JIMMessage, JIMMessageError

@pytest.fixture
def message():
    return JIMMessage("John", "busy")

class TestJIMMessage:
    def test_base(self, message):
        expect = {
            "action": "probe",
            "time": time.time()
        }
        msg = message._base("probe")
        assert expect.keys() == msg.keys()
        assert abs(expect["time"] - msg["time"]) < 0.1


