from figure import Figure


class Rectangle(Figure):

    def __init__(self, side_a: int | float, side_b: int | float):
        if side_a <= 0 or side_b <= 0:
            raise ValueError("Rectangle sides must be greater than 0")
        self.side_a = side_a
        self.side_b = side_b

    @property
    def area(self):
        return self.side_a * self.side_b

    @property
    def perimeter(self):
        return (self.side_a + self.side_b) * 2

