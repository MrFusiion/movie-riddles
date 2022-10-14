from hashlib import sha1
import os

def check():
    assert os.path.exists('solution.txt')

    with open('solution.txt') as file:
        solution = file.read().strip().lower().encode('utf-8')

    assert sha1(solution).hexdigest() == '345c26a5cce9e8c50e1c6bd3c7b4826110fd16d9'
