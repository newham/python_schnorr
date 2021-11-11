import mod
from point import Point
# by liuhan 2021-11-11
# 基本实现了椭圆曲线的加法、乘法的快速运算，测试用的曲线为secp256k1


class ECC:
    def __init__(self, a, b, p, G) -> None:
        self.a = a
        self.b = b
        self.p = p
        self.G = G

    def curve(self, x, y):
        return ((y**2) - (x**3 + self.a*x+self.b)) % self.p == 0

    def curve_plus(self, x1, y1, x2, y2):
        if x1 != x2 and y1 != y2:
            k = mod.divide_mod(y2-y1, x2-x1, self.p)
        else:
            k = mod.divide_mod((3*x1**2+self.a), 2*y1, self.p)
        x3 = (k**2-x1-x2) % self.p
        y3 = (k*(x1-x3)-y1) % self.p
        return x3, y3

    def curve_g_times(self, n):
        return self.curve_times(self.G.x, self.G.y, n)

    def curve_times(self, x, y, n):  # 递归求解100为1组的加法！加速效果明显（d的指数级增加，d=2时，可得到2的指数级加速！）
        # x,y 必须是曲线上的点，否则加法无意义
        d = 2
        if n <= d:
            for i in range(n):
                x, y = self.curve_plus(x, y, x, y)
            return x, y
        else:
            x1, y1 = self.curve_times(
                x, y, int(n/d))  # 商为下一轮递归的输入
            x2, y2 = self.curve_times(
                x, y, n % d)  # 余数为需要加另一个半结果
            return self.curve_plus(x1, y1, x2, y2)

    def get_line(self, x1, y1, x2, y2):
        # x1,y1 = 0,2.645751311064591
        # x2,y2 = -1.912931182772389,0

        a = (y1-y2)/(x1-x2)
        b = (x1*y2-x2*y1)/(x1-x2)

        print("y=%sx+%s" % (a, b))
        return a, b

    def test(self):
        a, b = self.get_line(0, 2.645751311064591, -1.912931182772389, 0)
        print(self.curve_plus(a, b, 0, 2.645751311064591, -1.912931182772389, 0))

    def test_plus(self, x0, y0):
        x1, y1 = self.curve_plus(x0, y0, x0, y0)
        print('x1=', x1, 'y1=', y1)
        print(self.curve(x1, y1))

    def test_times(self, x0, y0, n):
        x2, y2 = self.curve_times(x0, y0, n)
        print('x2=', hex(x2), 'y2=', hex(y2))
        print(self.curve(x2, y2))

    def test_g_times(self, n):
        x2, y2 = self.curve_g_times(n)
        print('x2=', hex(x2), 'y2=', hex(y2))
        print(self.curve(x2, y2))


def get_secp256k1():
    # 返回 a, b, p, x0, y0
    return 0, 7, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F, Point(0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


if __name__ == '__main__':
    ecc = ECC(*get_secp256k1())  # *表示可变参数

    k = 0xab12a0c79dc2e17f4950c7dbea2784c257acfb1fc6f4dc9afee5d3d75541ff35
    ecc.test_g_times(k)
