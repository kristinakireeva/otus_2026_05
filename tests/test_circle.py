from src.circle import Circle
import pytest


@pytest.mark.parametrize(
    ("radius", "area", "perimeter"),
    [
        pytest.param(3, 28.274333882308138, 18.84955592153876, id='integer'),
        pytest.param(3.5, 38.48451000647496, 21.991148575128552, id='float')
    ]
)
def test_circle_area(radius, area, perimeter):
    r = Circle(radius)
    assert r.area == area
    assert r.perimeter == perimeter


def test_circle_invalid_radius():
    with pytest.raises(ValueError):
        Circle(-3)
