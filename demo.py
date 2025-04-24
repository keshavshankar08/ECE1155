from CredentialStuffing.CredentialStuffing import CredentialStuffing
from DictionaryAttack.DictionaryAttack import dictionary_attack_hash, hash_password
import os
from RainbowTables.RainbowTableAttack import run_rainbow_table
import hashlib

# Get user input of username, password, and algorithm to use
username = input("Enter a username: ")
password = input("Enter a password: ")
print("Choose an attack algorithm to use:")
print("\t(cs) Credential Stuffing")
print("\t(d) Dictionary")
print("\t(rt) Rainbow Table")
algorithm = input("Enter your choice: ")

# Run the corresponding algorithm
if algorithm == "cs":
    print("Running credential stuffing...")
    cs = CredentialStuffing("CredentialStuffing/usernames.gz.b64", "CredentialStuffing/passwords.gz.b64")
    ip_switch_delay = input("Enter IP switch delay (in seconds): ")
    base_delay_per_check = input("Enter base delay per check (in seconds): ")
    variation_limit = input("Enter variation try limit (0-7): ")

    if(ip_switch_delay == "" or base_delay_per_check == "" or variation_limit == ""):
        success, matches, sim_time, real_time, varied = cs.start_attack(username, password)
    else:
        success, matches, sim_time, real_time, varied = cs.start_attack(username, password, float(ip_switch_delay), float(base_delay_per_check), int(variation_limit))

    if success:
        print(f"Attack successfully used the database and found {matches} matches in {round(sim_time, 2)} seconds, but would have taken {round(real_time, 2)} seconds in real life.")
    elif varied:
        print(f"Variations were needed to try to find matches. {matches} matches were found in {round(sim_time, 2)} seconds, which would have taken {round(real_time, 2)} seconds in real life.")
elif algorithm == "d":
    print("Running dictionary attack...")
    chosen_hash = input("Enter the target hash: ")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dictionary_file = os.path.join(script_dir, "DictionaryAttack/rockyou.txt")
    guess_rate = int(input("Enter estimated guess rate (guesses per second): "))
    target_hash = hash_password(password, chosen_hash)
    found, attempts, estimated_time, simulation_time, cracked_password = dictionary_attack_hash(
        target_hash, dictionary_file, chosen_hash, guess_rate
    )
    
    if found is None:
       print("Error: The dictionary file was not found.")
       exit(0)
    
    if found:
        print(f"\nPassword found after {attempts} attempts.")
        print(f"Cracked password: {cracked_password}")
    else:
        print("\nPassword not found in the dictionary.")
    
    print(f"Estimated time to crack: {estimated_time:.6f} seconds (at {guess_rate} guesses/sec).")
    print(f"Actual simulation time: {simulation_time:.6f} seconds.")
    pass
elif algorithm == "rt":
    print("Running rainbow table attack...")
    algorithm = input("select algorithm: MD5 or SHA1 ")
    if algorithm == "MD5":
        run_rainbow_table("md5-rainbow-short.rt", hashlib.md5)
    elif algorithm == "SHA1":
        run_rainbow_table("sha1-rainbow-short.rt", hashlib.sha1)