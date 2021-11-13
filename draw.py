# 过两点的直线
def get_line(self, x1, y1, x2, y2):
    # x1,y1 = 0,2.645751311064591
    # x2,y2 = -1.912931182772389,0

    a = (y1-y2)/(x1-x2)
    b = (x1*y2-x2*y1)/(x1-x2)

    print("y=%sx+%s" % (a, b))
    return a, b


def test_show(self):
    a, b = self.get_line(0, 2.645751311064591, -1.912931182772389, 0)
    print(self.curve_plus(a, b, 0, 2.645751311064591, -1.912931182772389, 0))
