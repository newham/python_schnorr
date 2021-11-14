import tinyec.ec as ec
import tinyec.registry as reg


def test_1():
    c = reg.get_curve("secp192r1")
    # c = reg.get_curve("secp256k1")
    k = 0xab12a0c79dc2e17f4950c7dbea2784c257acfb1fc6f4dc9afee5d3d75541ff35
    p1 = k * c.g
    print(hex(p1.x), hex(p1.y))
    pass


def test_secp256k1():
    a = 0
    b = 7
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # 大素数
    g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)  # 基点
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 1
    f = ec.SubGroup(p, g, n, h)
    c = ec.Curve(a, b, f, name='secp256k1')
    k = 0xab12a0c79dc2e17f4950c7dbea2784c257acfb1fc6f4dc9afee5d3d75541ff35
    p1 = k * c.g
    print(hex(p1.x), hex(p1.y))


if __name__ == "__main__":
    test_secp256k1()
    pass
