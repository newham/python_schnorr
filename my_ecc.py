import mod
# by liuhan 2021-11-11
# 基本实现了椭圆曲线的加法、乘法的快速运算，测试用的曲线为secp256k1


def curve(a, b, p, x, y):
    return ((y**2) - (x**3 + a*x+b)) % p == 0


def curve_plus(a, p, x1, y1, x2, y2):
    if x1 != x2 and y1 != y2:
        k = mod.divide_mod(y2-y1, x2-x1, p)
    else:
        k = mod.divide_mod((3*x1**2+a), 2*y1, p)
    x3 = (k**2-x1-x2) % p
    y3 = (k*(x1-x3)-y1) % p
    return x3, y3


def curve_times(a, p, x, y, n):  # 递归求解100为1组的加法！加速效果明显（d的指数级增加，d=2时，可得到2的指数级加速！）
    d = 2
    if n <= d:
        for i in range(n):
            x, y = curve_plus(a, p, x, y, x, y)
        return x, y
    else:
        x1, y1 = curve_times(a, p, x, y, int(n/d))  # 商为下一轮递归的输入
        x2, y2 = curve_times(a, p, x, y, n % d)  # 余数为需要加另一个半结果
        return curve_plus(a, p, x1, y1, x2, y2)


def get_line(x1, y1, x2, y2):
    # x1,y1 = 0,2.645751311064591
    # x2,y2 = -1.912931182772389,0

    a = (y1-y2)/(x1-x2)
    b = (x1*y2-x2*y1)/(x1-x2)

    print("y=%sx+%s" % (a, b))
    return a, b


def test():
    a, b = get_line(0, 2.645751311064591, -1.912931182772389, 0)
    print(curve_plus(a, b, 0, 2.645751311064591, -1.912931182772389, 0))


def test_plus(a, b, p, x0, y0):
    x1, y1 = curve_plus(a, p, x0, y0, x0, y0)
    print('x1=', x1, 'y1=', y1)
    print(curve(a, b, p, x1, y1))


def test_times(a, b, p, x0, y0, n):
    x2, y2 = curve_times(a, p, x0, y0, n)
    print('x2=', hex(x2), 'y2=', hex(y2))
    print(curve(a, b, p, x2, y2))


def get_secp256k1():
    # 返回 a, b, p, x0, y0
    return 0, 7, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F, 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def test_secp256k1():
    a, b, p, x0, y0 = get_secp256k1()
    # k<p，随机生成得到的256位二进制数
    k = 0xab12a0c79dc2e17f4950c7dbea2784c257acfb1fc6f4dc9afee5d3d75541ff35

    # test_plus(a,b,p,x0,y0)
    test_times(a, b, p, x0, y0, k)


if __name__ == '__main__':
    test_secp256k1()
