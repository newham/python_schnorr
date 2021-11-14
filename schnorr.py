# schnorr 签名、群签名
from util import rand_big, sha256_str, sha256_int
# from ec import EllipseCurve, get_secp256k1
import tinyec.ec as ec  # 用第三方库实现
from tinyec.ec import Point
from typing import Tuple


def get_secp256k1():
    a = 0
    b = 7
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # 大素数
    g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)  # 基点
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # order
    h = 1  # Cofactor
    f = ec.SubGroup(p, g, n, h)
    c = ec.Curve(a, b, f, name='secp256k1')
    return c


class Schnorr:

    def __init__(self, ec: ec.Curve) -> None:
        self.ec = ec
        pass

    # Schnorr签名使用点R 和标量 s 来生成签名，R 是椭圆曲线上的一随机点： R=k\cdot G，签名第2部分为：s = k + H(P,R,m)*sk , 其中sk 为私钥， P = sk*G 为公钥，m 为消息.
    def setup(self, n_k, n_sk) -> Tuple[int, int, Point, Point]:
        k = rand_big(n_k)
        sk = rand_big(n_sk)
        R = k*self.ec.g
        P = sk*self.ec.g
        return k, sk, R, P

    def hash(self, P: Point, R: Point, M: str) -> int:
        return sha256_int(sha256_int(P.x+P.y)+sha256_int(R.x+R.y)+sha256_str(M))

    # 签名
    def sign(self, k: int, sk: int, P: Point, R: Point, M: str) -> Tuple[int, int]:
        e = self.hash(P, R, M)
        s = k + e*sk
        return e, s

    # 验证签名: s*G =R+H(P,R,m)*P
    def validate(self, e: int, s: int, P: Point, R: Point) -> bool:
        s1 = s * self.ec.g
        s2 = R + e*P
        return s1 == s2


if __name__ == "__main__":
    schnorr = Schnorr(get_secp256k1())
    k, sk, R, P = schnorr.setup(256, 256)
    e, s = schnorr.sign(k, sk, P, R, 'Liu Han')
    print(schnorr.validate(e, s, P, R))
