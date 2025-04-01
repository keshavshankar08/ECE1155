from CredentialStuffing.CredentialStuffing import CredentialStuffing

# ---------- CredentialStuffing Module Example ----------
# Create the class object
cs = CredentialStuffing("CredentialStuffing/usernames.gz.b64", "CredentialStuffing/passwords.gz.b64") 

# User inputs
username = "admin"
password = "abc123"

# Start attack with user inputs
results = cs.start_attack(username, password)

# Unpack the results (success:bool, total_matches:int, search_time:float)
success, total_matches, search_time, variation_enabled = results 

# Print results
print(f"Attack Successful: {success}, Total Matches: {total_matches}, Search Time (sec): {search_time:.2f}, Variation Enabled: {variation_enabled}")
if success:
    print(f"FATAL! Your credentials were found in {total_matches} locations in a time of {search_time:.2f} seconds.")
elif not success and variation_enabled and total_matches > 0:
    print(f"WARNING! Your credentials were not found, but close hits were found in {total_matches} locations in a time of {search_time:.2f} seconds.")
elif not success and variation_enabled and total_matches == 0:
    print(f"SUCCESS! Your credentials were not found, and no close hits were found in a time of {search_time:.2f} seconds.") 