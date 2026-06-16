import math
from figure import Figure


class Circle(Figure):

        def __init__(self, radius: int | float):
            if radius <= 0:
                raise ValueError("Circle radius must be greater than 0")
            self.radius = radius

        @property
        def area(self):
            return math.pi * (self.radius ** 2)

        @property
        def perimeter(self):
            return 2 * math.pi * self.radius

