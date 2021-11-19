from bloom_filter import BloomFilter
from util import cost_time, rand_big_hex, rand_big_str


def demo():
    bloom = BloomFilter(max_elements=100, error_rate=0.1)
    bloom.add('https://www.tianyancha.com/company/23402373')
    bloom.add('https://www.tianyancha.com/company/23402372')
    bloom.add('https://www.tianyancha.com/company/2340231')
    bloom.add('https://www.tianyancha.com/company/23402')
    bloom.add('https://www.tianyancha.com/company/234')
    bloom.add('https://www.tianyancha.com/company/234023')

    s1 = 'https://www.tianyancha.com/company/23402373'
    print(s1 in bloom)
    pass


def test_bloom(n: int):
    bloom = BloomFilter(max_elements=n*10, error_rate=0.01)
    test_data = []
    for i in range(n):
        test_data.append(rand_big_str(256))
        bloom.add(test_data[i])
    c = 0
    for i in range(n):
        if test_data[i] in bloom:
            c += 1
    print(c == n)
    pass


if __name__ == '__main__':
    cost_time('test_bloom', test_bloom, 1000)
