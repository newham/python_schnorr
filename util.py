# by liuhan 2021-11-11
# 工具函数
import hashlib
import random
import secrets
import time


def big_prime():
    pass


def rand_diff_int_list(max: int, n: int) -> int:
    return random.sample(range(0, max), n)


def rand_int(max: int) -> int:
    return random.randint(1, max)


def rand_big(n: int) -> int:
    return secrets.randbits(n)


def rand_big_str(n: int) -> int:
    return str(rand_big(n))


def rand_big_hex(n: int) -> str:
    return sha256_hex(rand_big_str(n))


def sha256_str(str: str) -> int:
    f = hashlib.sha256()
    f.update(str.encode('utf-8'))
    return int.from_bytes(f.digest(), byteorder='big')  # byte 转 int


def sha256_hex(str: str) -> str:
    return hashlib.sha256(str.encode('utf-8')).hexdigest()


def sha256_int(i: int) -> int:
    return sha256_str(str(i))


def cost_time(tag: str, f, *args) -> float:
    start_time = time.time()
    f(*args)
    elapse_time = time.time() - start_time
    print(tag, 'cost time(s):', elapse_time)
    return elapse_time


if __name__ == "__main__":
    # print(hex(rand_big(256)))
    print(sha256_str('liuhan'))
    print(sha256_int(123))
