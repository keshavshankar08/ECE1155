import hashlib
import time
import os

def hash_password(password, algorithm="md5"):
    """
    hashes a password with the specified algorithm
    
    :param password: plaintext password
    :param algorithm: hash algorithm - either "md5" or "sha256"
    :return: hashed password as a hexadecimal string
    """
    password_bytes = password.encode()
    if algorithm.lower() == "md5":
        return hashlib.md5(password_bytes).hexdigest()
    elif algorithm.lower() == "sha256":
        return hashlib.sha256(password_bytes).hexdigest()
    else:
        raise ValueError("Unsupported algorithm. Use 'md5' or 'sha256'.")

def dictionary_attack_hash(target_hash, dictionary_file, algorithm="md5", guess_rate=100000):
    """
    simulates dictionary atack by reading candidate passwords from a dictionary file,
    hashing each, and comparing against target hash.
    
    :param target_hash: hash of the target password
    :param dictionary_file: path to dictionary file
    :param algorithm: hash algorithm used - either "md5" or "sha256"
    :param guess_rate: estimated number of guesses per second
    :return: tuple (found, attempts, estimated_time, simulation_time, cracked_password)
             where:
              - found: bool indicating if the password was found
              - attempts: number of candidates checked
              - estimated_time: estimated cracking time (in seconds) at the given guess rate
              - simulation_time: actual time (in seconds) taken by the simulation (using time.time())
              - cracked_password: password if found, otherwise None
    """
    attempts = 0
    found = False
    cracked_password = None

    start_time = time.time()
    try:
        with open(dictionary_file, 'r', encoding='latin-1') as file:
            for line in file:
                candidate = line.strip()
                attempts += 1
                candidate_hash = hash_password(candidate, algorithm)
                if candidate_hash == target_hash:
                    found = True
                    cracked_password = candidate
                    break
    except FileNotFoundError:
        print(f"Error: The dictionary file '{dictionary_file}' was not found.")
        return None, None, None, None, None

    simulation_time = time.time() - start_time
    estimated_time = attempts / guess_rate

    return found, attempts, estimated_time, simulation_time, cracked_password

def main():
    target_password = input("Enter the target plaintext password: ")
    algorithm = input("Enter hash algorithm (md5/sha256) [default md5]: ") or "md5"

    # compute target hash
    target_hash = hash_password(target_password, algorithm)
    print(f"Target hash ({algorithm}): {target_hash}")

    # get dictionary file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_file = os.path.join(script_dir, "rockyou.txt")
    guess_rate = 100000  # guesses per second

    # run simulation
    found, attempts, estimated_time, simulation_time, cracked_password = dictionary_attack_hash(
        target_hash, dictionary_file, algorithm, guess_rate
    )
    
    if found is None:
        return  # exit if dictionary was not found in directory
    
    if found:
        print(f"\nPassword found after {attempts} attempts.")
        print(f"Cracked password: {cracked_password}")
    else:
        print("\nPassword not found in the dictionary.")
    
    print(f"Estimated time to crack: {estimated_time:.6f} seconds (at {guess_rate} guesses/sec).")
    print(f"Actual simulation time: {simulation_time:.6f} seconds.")

if __name__ == "__main__":
    main()
