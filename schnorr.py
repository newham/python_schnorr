# schnorr 签名、群签名
from point import Point
from util import rand_big, sha256_str, sha256_int
from ec import EllipseCurve, get_secp256k1
from typing import Tuple


class Schnorr:

    def __init__(self, a, b, p, G) -> None:  # a,b,p,G 是椭圆曲线的参数
        self.ec = EllipseCurve(a, b, p, G)
        pass

    # Schnorr签名使用点R 和标量 s 来生成签名，R 是椭圆曲线上的一随机点： R=k\cdot G，签名第2部分为：s = k + H(P,R,m)*sk , 其中sk 为私钥， P = sk*G 为公钥，m 为消息.
    def setup(self, n_k, n_sk) -> Tuple[int, int, Point, Point]:
        k = rand_big(n_k)
        sk = rand_big(n_sk)
        R = self.ec.curve_g_times(k)
        P = self.ec.curve_g_times(sk)
        return k, sk, R, P

    # 签名
    def sign(self, k: int, sk: int, P: Point, R: Point, M: str) -> Tuple[int, int]:
        e = sha256_int(P.sha256()+R.sha256()+sha256_str(M))
        s = k + e*sk
        return e, s

    # 验证签名: s*G =R+H(P,R,m)*P
    def validate(self, e: int, s: int, P: Point, R: Point) -> bool:
        s1 = self.ec.curve_g_times(s)
        s2 = self.ec.curve_plus(R, self.ec.curve_times(P, e))
        s1.print('s1')
        s2.print('s2')
        return s1.compare(s2)


if __name__ == "__main__":
    schnorr = Schnorr(*get_secp256k1())
    k, sk, R, P = schnorr.setup(256, 256)
    e, s = schnorr.sign(k, sk, P, R, 'Liu Han')
    print(schnorr.validate(e, s, P, R))
