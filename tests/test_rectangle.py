from src.rectangle import Rectangle
import pytest


@pytest.mark.parametrize(
    ("side_a", "side_b", "area", "perimeter"),
    [
        pytest.param(3, 5, 15, 16, id='integer'),
        pytest.param(3.5, 5.5, 19.25, 18.0, id='float')
    ]
)
def test_rectangle_area(side_a, side_b, area, perimeter):
    r = Rectangle(side_a, side_b)
    assert r.area == area
    assert r.perimeter == perimeter


def test_rectangle_invalid_sides():
    with pytest.raises(ValueError):
        Rectangle(-3, 5)


# Новый тест, использующий созданную фикстуру
def test_rectangle_with_fixture(default_rectangle):
    assert default_rectangle.area == 15
    assert default_rectangle.perimeter == 16
    assert default_rectangle.side_a == 3

