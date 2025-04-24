from CredentialStuffing import CredentialStuffing
import itertools
import csv
import os

# ---------- Initialize ----------
print("Loading Dataset...")
cs = CredentialStuffing("CredentialStuffing/usernames.gz.b64", "CredentialStuffing/passwords.gz.b64")
print(f"Loaded {len(cs.usernames):,} usernames and {len(cs.passwords):,} passwords.\n")

# ---------- Test Parameters ----------
test_cred_pairs = [
    ("admin", "abc123"),
    ("keshavshankar08", "i@heart@pitt@123")
]

ip_delays = [i for i in range(0, 61, 15)]  # 0 to 60 seconds in 5 parts
base_delays = [i for i in range(0, 8641, 1728)]  # 0 to 8640 in 5 parts
variation_limits = list(range(8))  # 0 to 7

# ---------- Run Tests ----------
print("Running Simulation...\n")

for username, password in test_cred_pairs:
    print(f"Testing with Username: {username}, Password: {password}")
    safe_user = username.replace("@", "_").replace(".", "_")
    filename = f"results_{safe_user}.csv"

    results = []  # Store all results in memory

    print("Username\tPassword\tIP_Delay\tBase_Delay\tVar_Limit\tSuccess\tMatches\tSimTime\tRealTime\tAvgTime\tVariation")

    for ip_d, base_d, var_l in itertools.product(ip_delays, base_delays, variation_limits):
        success, matches, sim_time, real_time, varied = cs.start_attack(
            username,
            password,
            ip_switch_delay=ip_d,
            base_delay_per_check=base_d,
            variation_limit=var_l
        )

        avg_time_per_search = real_time / matches if matches > 0 else 0

        results.append([
            username, password,
            ip_d, base_d, var_l,
            int(success), matches, sim_time, real_time, avg_time_per_search, int(varied)
        ])

        print(f"{username}\t{password}\t{ip_d}\t{base_d}\t{var_l}\t{int(success)}\t{matches}\t{sim_time}\t{real_time}\t{avg_time_per_search}\t{int(varied)}")

    # Write all results to the file at once
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Username", "Password",
            "IP_Delay", "Base_Delay", "Var_Limit",
            "Success", "Matches", "SimTime", "RealTime", "AvgTime", "Variation"
        ])
        writer.writerows(results)

    print(f"Saved results to {filename} ✅")
