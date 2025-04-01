from CredentialStuffing.CredentialStuffing import CredentialStuffing

# ----- CredentialStuffing Module Example -----
# Create the class object
cs = CredentialStuffing("CredentialStuffing/usernames.gz.b64", "CredentialStuffing/passwords.gz.b64") 

# User inputs
username = "admin"
password = "1234"

# Start attack with user inputs
results = cs.start_attack(username, password)

# Unpack the results (success:bool, total_matches:int, search_time:float)
success, total_matches, search_time = results 

# Print results
if (success):
    print(f"Attack successful! Total matches: {total_matches}, Search time: {search_time:.2f} seconds")
else:
    print("Attack failed.")
