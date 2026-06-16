from src.square import Square
import pytest


@pytest.mark.parametrize(
    ("side_a", "area", "perimeter"),
    [
        pytest.param(3, 9, 12, id='integer'),
        pytest.param(3.5, 12.25, 14.0, id='float')
    ]
)
def test_square_area(side_a, area, perimeter):
    r = Square(side_a)
    assert r.area == area
    assert r.perimeter == perimeter


def test_square_invalid_sides():
    with pytest.raises(ValueError):
        Square(-3)
