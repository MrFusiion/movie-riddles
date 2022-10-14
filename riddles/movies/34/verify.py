from hashlib import sha1
import os

def check():
    assert os.path.exists('solution.txt')

    with open('solution.txt') as file:
        solution = file.read().strip().lower().encode('utf-8')

    assert sha1(solution).hexdigest() == '386a231f3dfd54d42a105187c3ff57c497c0ada3'
