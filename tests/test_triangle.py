from src.triangle import Triangle
import pytest


@pytest.mark.parametrize(
    ("side_a", "side_b", "side_c", "area", "perimeter"),
    [
        pytest.param(3, 4, 5, 6, 12, id='integer'),
        pytest.param(3.5, 4.5, 5.5, 7.854885024620029, 13.5, id='float')
    ]
)
def test_triangle_area(side_a, side_b, side_c, area, perimeter):
    r = Triangle(side_a, side_b, side_c)
    assert r.area == area
    assert r.perimeter == perimeter


def test_triangle_invalid_sides():
    with pytest.raises(ValueError):
        Triangle(-3,5, -9)

