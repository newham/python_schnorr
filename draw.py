# 过两点的直线
def get_line(x1, y1, x2, y2):
    # x1,y1 = 0,2.645751311064591
    # x2,y2 = -1.912931182772389,0

    a = (y1-y2)/(x1-x2)
    b = (x1*y2-x2*y1)/(x1-x2)

    print("y=%sx+%s" % (a, b))


def get_λ(x1, y1, x2, y2, a):
    if x1 != x2 or y1 != y2:
        return (y2-y1)/(x2-x1)
    else:
        return (3*x1**2+a)/(2*y1)


def P_P(x1, y1, x2, y2, λ):
    x3 = λ**2-x1-x2
    y3 = λ*(x1-x3)-y1
    return x3, -y3


def test_show():
    get_line(0, 2.645751311064591, -1.912931182772389, 0)
    get_line(0, 4, 2, 0)
    x1, y1 = -1, 2.4495
    x3, y3 = P_P(x1, y1, x1, y1, get_λ(x1, y1, x1, y1, 0))
    print(x3, y3)
    get_line(x1, y1, x3, y3)


if __name__ == "__main__":
    test_show()
