import pytest
from datetime import datetime, timedelta
from libminutaria import Timer

@pytest.fixture
def timer_fixture():
    timer = Timer(hours=0, minutes=0, seconds=5)
    # 2021-01-01 12:00:00
    timer._base = datetime(2021, 1, 1, 12, 0, 0, 0)
    timer._actualization = datetime(timer._base.year,
                                    timer._base.month,
                                    timer._base.day,
                                    timer._base.hour,
                                    timer._base.minute,
                                    timer._base.second,
                                    timer._base.microsecond)
    return timer

def test_convert_delta_to_datetime(timer_fixture):
    assert(timer_fixture._convert_delta_to_datetime() ==
           datetime(2021, 1, 1, 12, 0, 5, 0))

def test_rebase_current_time(timer_fixture):
    # Not really accurate but can't do better
    timer_fixture._rebase_current_time()
    # Check if _actualization was updated with a more
    # recent (greater) datetime
    assert(timer_fixture._actualization > timer_fixture._base)
    # Check if _actualized_delta was reduced
    assert(timer_fixture._actualized_delta < timer_fixture._delta)


def test_is_timing_reached(timer_fixture):
    # Set timer as if it has just begun
    # Sufficient with a 5sec timer to pass the test
    timer_fixture._base = datetime.now()
    assert(not timer_fixture.is_timing_reached())
    # Set timer as if it was ended for a long time
    # With a 5sec, the timer already ended to pass the test
    timer_fixture._base = datetime(2021, 1, 1, 12, 0, 0, 0)
    assert(timer_fixture.is_timing_reached())
