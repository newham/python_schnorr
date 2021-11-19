# schnorr 签名、群签名
# Setup:

# x := random number (aka private key) G := common point X := x * G (aka public key)

# Sign:

# r := random number (aka nonce) R := r G (aka commitment) e := Hash(R, X, message)(aka challenge) s := r + e x (aka response) return (R, X, s, message) ((s, e) aka signature)

# Verify:

# receive (R, X, s, message) e := Hash(R, X, message) S1 := R + e X S2 := s G return OK if S1 qeuals S2


from util import rand_big, rand_big_str, sha256_str, sha256_int, cost_time
# from ec import EllipseCurve, get_secp256k1
import tinyec.ec as ec  # 用第三方库实现椭圆曲线运算
from tinyec.ec import Point
from typing import List, Tuple  # 多类型返回
import time


def get_secp256k1():
    a = 0
    b = 7
    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # 大素数
    g = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
         0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)  # 基点

    # order(阶)
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    h = 1  # Cofactor
    f = ec.SubGroup(p, g, n, h)
    c = ec.Curve(a, b, f, name='secp256k1')
    return c


class PubKey():
    def __init__(self,  R: Point, P: Point) -> None:
        self.R = R
        self.P = P
        pass


class KeyPair():
    def __init__(self, k: int, sk: int, R: Point, P: Point) -> None:
        self.k = k
        self.sk = sk
        self.pk = PubKey(R, P)
        pass


class Signature():
    def __init__(self, h: int, s: int) -> None:
        self.h = h
        self.s = s
        pass


class Schnorr:

    def __init__(self, ec: ec.Curve) -> None:
        self.ec = ec
        pass

    # Schnorr签名使用点R 和标量 s 来生成签名，R 是椭圆曲线上的一随机点： R=k\cdot G，签名第2部分为：s = k + H(P,R,m)*sk , 其中sk 为私钥， P = sk*G 为公钥，m 为消息.
    def setup(self, k_n: int) -> KeyPair:  # n 为秘钥长度
        k = rand_big(k_n)
        sk = rand_big(k_n)
        R = k*self.ec.g
        P = sk*self.ec.g
        return KeyPair(k, sk, R, P)

    # 群签名，初始化，生成 聚合公钥
    def setup_mu(self, key_pairs: list) -> Tuple[PubKey, int]:
        # 计算聚合的公钥
        L_P = key_pairs[0].pk.P
        for i, key_pair in enumerate(key_pairs):
            if i > 0:
                L_P += key_pair.pk.P
        L = sha256_int(L_P.x+L_P.y)  # int
        for i, key_pair in enumerate(key_pairs):
            P_i = key_pair.pk.P
            R_i = key_pair.pk.R
            h = self.hash_i_P(L, P_i)
            if i == 0:
                P = h*P_i
                R = R_i
            else:
                P += h*P_i
                R += R_i
            pass
        return PubKey(R, P), L  # 注意这里的R、P变量顺序

    def hash_msg(self, P: Point, R: Point, M: str) -> int:
        return sha256_int(sha256_int(P.x+P.y)+sha256_int(R.x+R.y)+sha256_str(M))

    def hash_2P(self, P1: Point, P2: Point) -> int:
        return sha256_int(sha256_int(P1.x+P1.y)+sha256_int(P2.x+P2.y))

    def hash_i_P(self, i: int, P: Point) -> int:
        return sha256_int(i+P.x+P.y)

    # 签名
    def sign(self, key_pair: KeyPair, M: str) -> Signature:
        h = self.hash_msg(key_pair.pk.P, key_pair.pk.R, M)
        s = key_pair.k + h*key_pair.sk
        return Signature(h, s)

    # 群签名,PK是所有成员公共的公钥，L是所有公钥的hash，M是共享签名
    def sign_mu(self, key_pair: KeyPair, PK: PubKey, L: int, M: str) -> Tuple[int, int]:
        P_i = key_pair.pk.P
        H = self.hash_msg(PK.P, PK.R, M)
        h = self.hash_i_P(L, P_i)
        s_i = key_pair.k + H*h*key_pair.sk
        return H, s_i

    # 验证签名: s*G =R+H(P,R,m)*P
    def validate(self, sign: Signature, pk: PubKey) -> bool:
        s1 = sign.s * self.ec.g
        s2 = pk.R + sign.h * pk.P
        return s1 == s2

    def validate_group(self, pks: list, signs: list) -> bool:
        s = signs[0].s
        R = pks[0].R
        h_P = signs[0].h*pks[0].P
        for i, sign in enumerate(signs):
            if i > 0:  # 第一个已经赋值了，跳过
                s += sign.s
                R += pks[i].R
                h_P += sign.h*pks[i].P
        return s * self.ec.g == R + h_P


def test_single(schnorr: Schnorr):
    key_pair = schnorr.setup(256)
    sign = schnorr.sign(key_pair, 'Liu Han')
    print(schnorr.validate(sign, key_pair.pk))
    pass


def test_group(schnorr: Schnorr, n: int):
    # 测试群签名
    pks = []
    signs = []
    for i in range(n):
        key_pair = schnorr.setup(256)
        sign = schnorr.sign(key_pair, rand_big_str(128))
        pks.append(key_pair.pk)
        signs.append(sign)
    print(schnorr.validate_group(pks, signs))


def test_mu(schnorr: Schnorr, n: int):
    start_time = time.time()
    # 测试群签名 MuSig
    key_pairs = []
    for i in range(n):
        key_pair = schnorr.setup(256)
        key_pairs.append(key_pair)
    PK, L = schnorr.setup_mu(key_pairs)
    s = 0
    H = 0
    print('setup', 'cost time(s):', time.time() - start_time)
    start_time = time.time()
    for key_pair in key_pairs:
        H, s_i = schnorr.sign_mu(key_pair, PK, L, 'Liu Han')
        s += s_i
    print('sign', 'cost time(s):', time.time() - start_time)
    start_time = time.time()
    print(s*schnorr.ec.g == PK.R+H*PK.P)
    print('validate', 'cost time(s):', time.time() - start_time)


if __name__ == "__main__":
    schnorr = Schnorr(get_secp256k1())
    # cost_time('test_single', test_single, schnorr)
    cost_time('test_group', test_group, schnorr, 100)
    # cost_time('test_mu', test_mu, schnorr, 1000)

## test_mu 1000 ##
# setup cost time(s): 57.31436896324158
# sign cost time(s): 0.005015134811401367
# True
# validate cost time(s): 0.07626700401306152
# test_mu cost time(s): 57.39590811729431
