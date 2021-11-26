# setup 输入m个int，参数n，建立hash tree
# validate 输入n个int，输出bool，是否存在

# from: https://github.com/Tierion/pymerkletools

import hashlib
import time
from merkletools import MerkleTools

from util import cost_time, rand_big_str, rand_big_hex, sha256_hex


def demo():
    mt = MerkleTools()  # 默认sha256
    leafs = ['a', 'b', 'c', 'd', 'e', 'f']
    mt.add_leaf(leafs, do_hash=True)
    mt.make_tree()
    i = 1
    proof = mt.get_proof(i)  # 将证明作为给定索引处叶的哈希对象数组返回。如果树未就绪或给定索引中不存在叶，则返回null。
    # '\xca\x97\x81\x12\xca\x1b\xbd\xca\xfa\xc21\xb3\x9a#\xdcM\xa7\x86\xef\xf8\x14|Nr\xb9\x80w\x85\xaf\xeeH\xbb'
    h = sha256_hex(leafs[i])
    proof_res = mt.validate_proof(mt.get_proof(
        i), mt.get_leaf(i), mt.get_merkle_root())
    print(proof_res)
    pass


def test_merkle_tree(m: int, n: int):
    start_time = time.time()
    leafs = []
    for i in range(m):
        leafs.append(rand_big_str(256))
    mt = MerkleTools()  # 默认sha256
    mt.add_leaf(leafs, do_hash=True)
    mt.make_tree()
    print('setup', 'cost time(s):', time.time() - start_time)
    start_time = time.time()
    c = 0
    for i in range(m):
        proof_res = mt.validate_proof(mt.get_proof(
            i), sha256_hex(leafs[i]), mt.get_merkle_root())
        if proof_res:
            c += 1
    print(c == m)
    print('validate', 'cost time(s):', time.time() - start_time)
    pass


if __name__ == "__main__":
    # cost_time('demo', demo)
    cost_time('test merkle tree', test_merkle_tree, 10000, 10000)
