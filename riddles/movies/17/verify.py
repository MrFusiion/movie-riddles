from hashlib import sha1
import os

def check():
    assert os.path.exists('solution.txt')

    with open('solution.txt') as file:
        solution = file.read().strip().lower().encode('utf-8')

    assert sha1(solution).hexdigest() == '46dcd4dd65b63d106b8cfb4aad906b23716cc613'
