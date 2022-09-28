# position.py
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.position = (x,y)

    def __eq__(self, other):
        return isinstance(other, Position) and \
            self.x == other.x and \
            self.y == other.y

    def __str__(self):
      return f"({self.x}, {self.y})"

    def __getitem__(self, key):
        return self.position[key]

    __repr__ = __str__


