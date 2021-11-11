# 求a/b mod p

# 计算 x的y次方 对mod取模
def power_mod(x, y, mod):
    r = 1
    while(y):
        if y & 1:
            r = (r * x) % mod
        x = (x * x) % mod
        y >>= 1

    return r

# 利用费马小定理
# 来源：https://blog.csdn.net/qq_29921623/article/details/100559916
def divide_mod(a, b, p):
    return ((a % p) * power_mod(b, (p-2), p)) % p


if __name__ == "__main__":
    a = 199
    b = 177
    p = 67
    print(a * b % p)
    print(((a % p)*(b % p)) % p)
    print(divide_mod(4,3,1000000007))
