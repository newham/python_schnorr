# 二维平面上的点
from util import sha256_int


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        pass

    def print(self, name: str) -> None:
        print(name, 'x =', hex(self.x), ',', 'y =', hex(self.y))
        pass

    def sha256(self) -> int:
        return sha256_int(self.x + self.y)

    def compare(self, P) -> bool:
        return self.x == P.x and self.y == P.y
