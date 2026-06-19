import time

from raspal.throttle import AutoThrottle


def test_initial_delays():
    t = AutoThrottle(min_delay=0.5, max_delay=60.0)
    assert t.current_delays == {}


def test_wait_does_not_block_on_first_call():
    t = AutoThrottle(min_delay=10.0)
    start = time.time()
    t.wait("scrapling")
    elapsed = time.time() - start
    assert elapsed < 1.0  # Should not block on first call


def test_record_doubles_on_429():
    t = AutoThrottle(min_delay=1.0, max_delay=100.0)
    t.record("scrapling", 429)
    assert t.current_delays["scrapling"] == 2.0
    t.record("scrapling", 429)
    assert t.current_delays["scrapling"] == 4.0


def test_record_decays_on_200():
    t = AutoThrottle(min_delay=1.0, max_delay=100.0)
    t.record("scrapling", 429)  # doubles to 2.0
    t.record("scrapling", 200)  # should decay
    assert t.current_delays["scrapling"] < 2.0
    assert t.current_delays["scrapling"] >= 1.0


def test_record_respects_max():
    t = AutoThrottle(min_delay=1.0, max_delay=10.0)
    for _ in range(10):
        t.record("scrapling", 429)
    assert t.current_delays["scrapling"] == 10.0


def test_record_respects_min():
    t = AutoThrottle(min_delay=5.0, max_delay=100.0)
    for _ in range(10):
        t.record("scrapling", 200)
    assert t.current_delays["scrapling"] == 5.0


def test_reset():
    t = AutoThrottle(min_delay=1.0)
    t.record("scrapling", 429)
    t.reset("scrapling")
    assert t.current_delays["scrapling"] == 1.0


def test_context_manager():
    with AutoThrottle() as t:
        t.record("scrapling", 200)
        assert "scrapling" in t.current_delays
    assert t._closed is True


def test_close():
    t = AutoThrottle()
    t.record("scrapling", 200)
    t.close()
    # After close, wait should do nothing
    start = time.time()
    t.wait("scrapling")
    assert time.time() - start < 0.1
