"""Unit tests of robot.geometry, run with: python -m pytest tests"""
import pytest

from robot.geometry import turn_angle


@pytest.mark.parametrize("current, target, expected", [(-2, 2, 180), (0, 1, 45), (-1, -3, -90), (3, 1, -90), (1, 3, 90)])
def test_turn_angle_from_beacon(current, target, expected):
    """A robot 2.5 m in front of a beacon (at the arena centre) turns by the expected angle."""
    assert turn_angle(current, target, 2.5, 0) == pytest.approx(expected)
