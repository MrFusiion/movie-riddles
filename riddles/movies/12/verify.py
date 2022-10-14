from hashlib import sha1
import os

def check():
    assert os.path.exists('solution.txt')

    with open('solution.txt') as file:
        solution = file.read().strip().lower().encode('utf-8')

    assert sha1(solution).hexdigest() == 'fe7c657322b3964683019d675f0c393415a212f3'
