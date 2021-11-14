# by liuhan 2021-11-11
# 基本实现了椭圆曲线的加法、乘法的快速运算，测试用的曲线为secp256k1

import mod
from point import Point


# 椭圆曲线相关操作（加法、乘法）
class EllipseCurve:
    def __init__(self, a: int, b: int, p: int, G: Point) -> None:
        self.a = a
        self.b = b
        self.p = p
        self.G = G

    # 判断点是否在曲线上
    def curve(self, P: Point) -> bool:
        return ((P.y**2) - (P.x**3 + self.a*P.x+self.b)) % self.p == 0

    # 加法运算
    def curve_plus(self, P1: Point, P2: Point):
        if P1.x != P2.x and P1.y != P2.y:
            k = mod.divide_mod(P2.y-P1.y, P2.x-P1.x, self.p)
        else:
            k = mod.divide_mod((3*P1.x**2+self.a), 2*P1.y, self.p)
        x3 = (k**2-P1.x-P2.x) % self.p
        y3 = (k*(P1.x-x3)-P1.y) % self.p
        return Point(x3, y3)

    # 基点G的n次乘法运算
    def curve_g_times(self, n: int) -> Point:
        return self.curve_times(self.G, n)

    # 乘法运算
    # 递归求解100为1组的加法！加速效果明显（d的指数级增加，d=2时，可得到2的指数级加速！）
    # 自己始终无法实现高效的乘法，只能改用 pip install tinyec
    def curve_times(self, P: Point, n: int) -> Point:
        # x,y 必须是曲线上的点，否则加法无意义
        d = 2
        if n <= d:
            for i in range(n):
                P = self.curve_plus(P, P)
                # P.print('P')
            return P
        else:
            P1 = self.curve_times(self.curve_times(
                P, d), int(n/d))  # 商为下一轮递归的输入
            if n % d >= 0:
                P2 = self.curve_times(
                    P, n % d)  # 余数为需要加另外半个结果
                return self.curve_plus(P1, P2)
            else:
                return P1

    def curve_times_base(self, P: Point, n: int) -> Point:
        # x,y 必须是曲线上的点，否则加法无意义
        for i in range(n):
            P = self.curve_plus(P, P)
        return P

    def test_times(self, P: Point) -> None:
        n = 5
        P1 = self.curve_times(P, n)
        P2 = self.curve_times_base(P, n)
        P1.print('P1')
        P2.print('P2')

    def test_g_times(self, n):
        P = self.curve_g_times(n)
        P.print('P1')
        print(self.curve(P))

    def test_tongtai(self, a: int, b: int, c: int):
        A = self.curve_g_times(a)
        B = self.curve_g_times(b)
        C = self.curve_g_times(a+b)
        A_B = Point(A.x+B.x, A.y+B.y)
        A_B.print('A+B')
        C.print('C')
        print(A_B.compare(C))


def get_secp256k1():
    # 返回 a, b, p, x0, y0
    a = 0
    b = 7
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # 大素数
    G = Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
              0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)  # 基点
    return a, b, p, G


if __name__ == '__main__':
    ecc = EllipseCurve(*get_secp256k1())  # *表示可变参数
    k = 0xab12a0c79dc2e17f4950c7dbea2784c257acfb1fc6f4dc9afee5d3d75541ff35
    ecc.test_times(ecc.G)
    # ecc.test_g_times(k)
    # ecc.test_tongtai(4, 6, 10)
