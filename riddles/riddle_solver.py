from typing import Dict, Tuple;

from hashlib import sha1
import os, re, gzip
import urllib.request

import argparse


movies_dir_path = os.path.join(os.path.dirname(__file__), "movies")

dataset_url = "https://datasets.imdbws.com/title.basics.tsv.gz" # imdb movie dataset
title_index = 3 # column index for our title from the


def get_solution_path(dir: str) -> str:
    '''
    Create Gets the solution the solution path from a riddle folder.
    '''

    return os.path.join(dir, "solution.txt")


def get_solution(dir: str) -> str | None:
    '''
    Gets the solution from a riddle folder. None if not found.
    '''

    solution_file_path = get_solution_path(dir)

    if os.path.exists(solution_file_path):
        with open(solution_file_path, "r") as file:
            solution = file.read().strip()
            return solution != "" and solution or None

    return None


def get_hash(dir: str) -> str | None:
    '''
    Gets the hash from a riddle folder.
    '''

    verify_file_path = os.path.join(dir, "verify.py")

    if os.path.exists(verify_file_path):
        with open(verify_file_path, 'r') as verify_file:
            match = re.search(r"assert sha1\(solution\)\.hexdigest\(\) == '(.+)'", verify_file.read(), re.MULTILINE)
            return match and match.group(1) or None

    return None


def check_hash(hash: str, solution: str|None) -> bool:
    '''
    Checks if a solution is correct.
    '''

    return solution and sha1(solution.strip().lower().encode("utf-8")).hexdigest() == hash or False


def get_movie_dir(i: int):
    '''
    Gets the movie riddle folder by index.
    '''

    return os.path.join(movies_dir_path, f"{i:02d}")


def check_riddle(dir: str) -> bool:
    '''
    Checks if the riddle has the correct solution.
    '''

    return check_hash(get_hash(dir), get_solution(dir))


def print_line(length=30):
    '''
    Prints a line and a space.
    '''

    print("-" * length + "\n")


def download_data():
    '''
    Downloads the imdb movie dataset if its not found and unzips it.
    '''

    if os.path.exists('data.tsv'):
        return

    if not os.path.exists('data.tsv.gz'):

        print("Downloading movies dataset...")
        data_set_zipped = urllib.request.urlopen(dataset_url).read()

        with open('data.tsv.gz', 'wb') as data_zipfile:
            data_zipfile.write(data_set_zipped)

        print("Downloaded movies dataset.")
    
    print("Unzipping movies dataset...")

    with gzip.open('data.tsv.gz', 'rb') as data_zipfile:
        with open('data.tsv', 'wb') as data_file:
            data_file.write(data_zipfile.read())

    print("Unzipped movies dataset.")


def get_hashes_and_solutions() -> Tuple[Dict[str, str], Dict[str, str]]:
    '''
    Loops trough our movie riddles folder and searches its hash and solution if it exists.
    '''

    hashes = {}
    solutions = {}

    # get all hashes and allready found solutions
    for file in os.listdir(movies_dir_path):
        movie_dir = os.path.join(movies_dir_path, file)
        if os.path.isdir(movie_dir):

            if check_riddle(movie_dir): # check if solution is solved and if so store the solution
                solutions[int(file)] = get_solution(movie_dir)
            else: # 
                hashes[int(file)] = get_hash(movie_dir)

    return (hashes, solutions)


def find_solutions(hashes: Dict[str, str], solutions: Dict[str, str]):
    '''
    Loops trough the movies dataset and checks for each line if its a solution for one of our hashes.
    '''

    with open('data.tsv', 'r', encoding='utf-8') as file:
        lines = file.readlines()
            
        print("Start brute forcing movies riddles.")

        total = len(lines)
        print(f'total movies: {total}\n')

        for i in range(1, total-1):

            line = lines[i]
            title = line.split("\t")[title_index]

            for riddle, hash in hashes.items():
                if check_hash(hash, title): # check title hash with solution hash

                    # notify user we found a solution
                    print(f"Found solution for riddle: {int(riddle):02d}, hash: {hash}, solution: {title}")

                    solutions[riddle] = title # we found the solution so save it in our soltion dict
                    del hashes[riddle] # remove hash from our hases because we found the solution

                    break


def write_solutions(solutions: Dict[str, str]):
    '''
    Writes all the found solutions to their corresponding solution.txt file.
    '''

    print("Writing solutions...")

    for k, solution in solutions.items():
        solution_file_path = os.path.join(get_movie_dir(int(k)), "solution.txt")

        with open(solution_file_path, "w") as solution_file:
            solution_file.write(solution.strip())

    print("solutions writen.")


def check_solutions():
    '''
    Checks for all riddles if the found solutions is correct or wrong.
    This function is only useful, If you written some of your own solutions.
    '''
    
    print("check solutions:")

    for file in os.listdir(movies_dir_path):
        movie_dir_path = os.path.join(movies_dir_path, file)

        if os.path.isdir(movie_dir_path):

            solution = get_solution(movie_dir_path)
            hash = get_hash(movie_dir_path)

            correct = check_hash(hash, solution)

            print(f"\triddle: {file} | hash: {hash} | solution: {solution or '':<60} | [{correct and 'CORRECT' or 'WRONG'}]")


def clear_solutions():
    '''
    Clears all solutions.txt files. This function is useful if you want to start fresh,
    Or you have written some wrong solutions.
    '''

    for file in os.listdir(movies_dir_path):
        movie_dir_path = os.path.join(movies_dir_path, file)

        if os.path.isdir(movie_dir_path):

            solution_file_path = get_solution_path(movie_dir_path)

            if os.path.exists(solution_file_path):
                os.remove(solution_file_path)

    print("solutions cleared.")


def execute_riddle_solver():
    '''
    Runs the riddle solver. This will first download the imdb movies dataset and extract it if it is not found.
    It then searches for all hashes and their solution.txt if it exists.
    Then it looks for solutions for hashes that don't have solution.txt and writes them to the corresponding file.
    '''

    print("\nSearching for hashes and allready found solutions...")
    (hashes, solutions) = get_hashes_and_solutions()

    # stop if no hashes found
    if len(hashes.values()) == 0:
        print("No hashes to solve!")
        check_solutions()
        return

    # download and unzip data.tsv if it doesn't exist
    download_data()

    # print all hashes
    print(f"Hashes({len(hashes.values())}):")
    for k, hash in hashes.items():
        print(f"\triddle: {int(k):02d} | hash: {hash}")

    print_line()

    # brute force all riddles
    find_solutions(hashes, solutions)

    print_line()

    # print all found and non found solutions
    print(f"Solutions({len(solutions.values())}): ")
    print('\n'.join(f'\triddle: {riddle:0>2} | solution: {solution}' for riddle, solution in solutions.items()))
    
    print() # space

    print(f"Not found solutions({len(hashes.values())}): ")
    print('\n'.join(f'\triddle: {riddle:0>2} | hash: {hash}' for riddle, hash in hashes.items()))

    print_line()

    # write all found solutions to each movie riddle folder
    write_solutions(solutions)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Movie riddles solver and checker.')

    parser.add_argument("--solve", action="store_true",
                            help='solved the movie riddles')

    parser.add_argument("--check", action="store_true",
                            help='check if found solutions are correct')

    parser.add_argument("--clear", action="store_true",
                            help='clears all found solutions')

    args = parser.parse_args()

    if args.clear:
        clear_solutions()

    if args.check:
        check_solutions()
    elif args.solve:
        execute_riddle_solver()