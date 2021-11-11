# schnorr 签名、群签名

class signature:

    def __init__(self,a,b,p,G) -> None: # a,b,p 是椭圆曲线的参数
        self.a = a
        self.b = b
        self.p = p
        self.G = G
        pass

    
    def setup(): # 生成公私钥
        # 生成私钥 x = random number
        # 计算 X = x * G
        # 生成随机盐值 r = random number
        # 计算 R = r * G
        pass
