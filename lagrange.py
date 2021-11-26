from scipy.interpolate import lagrange
from numpy import poly1d
from util import cost_time, rand_big, rand_int, rand_diff_int_list
from itertools import combinations


def demo_polynomial():  # 构造多项式
    p1 = poly1d([1, 2, 3, 4, 5])
    print(p1)


def get_polynomial(a: list):  # 多项式,最后一项是常数项
    pass


def test():
    x = [1, 2, 3, 4, 7]
    y = [5, 7, 10, 3, 9]
    a = lagrange(x, y)
    print(a)
    print(a(1), a(2), a(3))
    print(a[0], a[2], a[3])


def Shamir():  # 作者：Alice-Bob https://www.bilibili.com/read/cv6674795/ 出处：bilibili
    # 1) 选择一个随机素数 p，并产生一个随机的 m-1 次多项式 (包括随机的常数有m个)
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    m = 50
    n = 100  # n>=m
    k = 20  # 偏移量
    a = [rand_int(10) for i in range(m-1)]  # 多项式系数
    M = rand_big(20)
    a.append(M)
    p1 = poly1d(a)  # 多项式，这里是浮点数，会溢出
    # print(p1)
    # print(len(a))
    print('M=', M)
    # print('a=', a, len(a))
    # 2) 选择 n 个互不相同的整数 1≤ x1,…,xn ≤ p-1
    x = rand_diff_int_list(n, n)
    # x = [rand_big(256) for i in range(n)]
    y = p1(x)
    # print(len(x), len(y))
    # print(x, y)
    # 3) m 个 秘密重构算法
    # print(len(x[k:m+k]))
    # print(x[0:m])
    # print(x[:m])
    # print(y[0:m])
    # print(y[:m])
    x_m = x[k:m+k]
    y_m = y[k:m+k]
    a = lagrange(x_m, y_m)
    print('a[0]=', a[0])
    print(M == a(0))
    pass


if __name__ == "__main__":
    # cost_time('lagrange', test)
    # cost_time('demo_polynomial', demo_polynomial)
    cost_time('Shamir', Shamir)
