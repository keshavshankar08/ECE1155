from rainbowtable import RainbowTable
import hashlib
import time
import os

def generate_table(table_name, alogorithm, chain_length):
    table = RainbowTable(alogorithm, chain_length)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_file = os.path.join(script_dir, table_name)
    table.load_rainbow_table(dictionary_file)
    return table

def crack_password(password : str, table: RainbowTable):
    first_hash = table.hash_function(password)
    return table.lookup(first_hash)

def main():
    md5_table = generate_table("md5_table_1m_1000.txt", hashlib.md5, 1000)
    while(True):
        password = input("Enter your password ")
        start_time = time.time()
        cracked_password = crack_password(password, md5_table)
        total_time = time.time() - start_time
        if cracked_password:
            print("This password was used to enter your account: ", cracked_password)
        else:
            print("Couldn't find matching hash!")
        print(f"total time: {total_time:.10f} seconds")
        

main()