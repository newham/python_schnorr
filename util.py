# by liuhan 2021-11-11
# 工具函数
import hashlib
import random
import secrets


def big_prime():
    pass


def rand_big(n):
    return secrets.randbits(n)


def sha256_str(str) -> int:
    f = hashlib.sha256()
    f.update(str.encode('utf-8'))
    return int.from_bytes(f.digest(), byteorder='big')  # byte 转 int


def sha256_int(i) -> int:
    return sha256_str(str(i))


if __name__ == "__main__":
    # print(hex(rand_big(256)))
    print(sha256_str('liuhan'))
    print(sha256_int(123))
