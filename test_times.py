import datetime
from times import time_range, compute_overlap_time
import pytest

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

    result = compute_overlap_time(large, short)

    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), 
                ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]

    assert result == expected

def test_no_overlap():
    range1 = time_range("2010-01-12 08:00:00", "2010-01-12 09:00:00")
    range2 = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")

    result = compute_overlap_time(range1, range2)

    expected = [('2010-01-12 10:00:00', '2010-01-12 09:00:00')]
    assert result == expected


def test_multiple_intervals():
    range1 = time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00", 2, 60)
    range2 = time_range("2010-01-12 09:30:00", "2010-01-12 10:30:00", 2, 60)

    result = compute_overlap_time(range1, range2)

    assert len(result) == len(range1) * len(range2)
    has_overlap = any(low < high for low, high in result)
    assert has_overlap


def test_touching_ranges():
    range1 = time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00")
    range2 = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")

    result = compute_overlap_time(range1, range2)

    expected = [('2010-01-12 10:00:00', '2010-01-12 10:00:00')]
    assert result == expected

def test_time_range_backwards():
    with pytest.raises(ValueError, match="end_time .* before start_time"):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")