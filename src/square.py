from figure import Figure


class Square(Figure):

    def __init__(self, side_a):
        if side_a <= 0:
            raise ValueError("Square sides can't be less than 0")

        self.side_a = side_a

    @property
    def perimeter(self):
        return (self.side_a + self.side_a) * 2

    @property
    def area(self):
        return self.side_a * self.side_a

