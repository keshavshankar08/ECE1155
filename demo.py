from CredentialStuffing.CredentialStuffing import CredentialStuffing

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
        success, matches, sim_time, real_time, varied = cs.start_attack(username, password, ip_switch_delay, base_delay_per_check, variation_limit)

    if success:
        print(f"Attack successfully used the database and found {matches} matches in {sim_time} seconds, but would have taken {real_time} seconds in real life.")
    elif varied:
        print(f"Variations were needed to try to find matches. {matches} matches were found in {sim_time} seconds, which would have taken {real_time} seconds in real life.")

elif algorithm == "d":
    print("Running dictionary attack...")
    pass
elif algorithm == "rt":
    print("Running rainbow table attack...")
    pass


# MANNY, ADD CODE HERE FOR BRUTE FORCE COMPARISON