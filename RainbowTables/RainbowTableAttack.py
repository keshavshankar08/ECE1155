from RainbowTables.rainbowtable import RainbowTable
import hashlib
import time
import os

def generate_table(table_name, alogorithm, chain_length):
    table = RainbowTable(alogorithm, chain_length)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_file = os.path.join(script_dir, table_name)
    table.load_rainbow_table_from_compressed(dictionary_file)
    return table

def crack_password(password : str, table: RainbowTable):
    first_hash = table.hash_function(password)
    return table.lookup(first_hash)

def run_rainbow_table(filename, algorithm, password):
    table = generate_table(filename, algorithm, 1000)
    start_time = time.time()
    cracked_password = crack_password(password, table)
    total_time = time.time() - start_time
    if cracked_password:
        print("This password was used to enter your account: ", cracked_password)
    else:
        print("Couldn't find matching hash!")
    print(f"total time: {total_time:.10f} seconds")


def main():
    while(True):
        algorithm = input("select algorithm: MD5 or SHA1 ")
        if algorithm == "MD5":
            run_rainbow_table("md5-rainbow-short.rt", hashlib.md5)
        elif algorithm == "SHA1":
            run_rainbow_table("sha1-rainbow-short.rt", hashlib.sha1)
