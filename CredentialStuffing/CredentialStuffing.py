"""
Author: Keshav Shankar
Date: April 1, 2025
Description: This script implements a CredentialStuffing class to simulate credential stuffing attacks.
"""
import threading
import time
import gzip
import base64

class CredentialStuffing:
    def __init__(self, usernames_file_path, passwords_file_path):
        self.username = ""                              # input username
        self.password = ""                              # input password
        self.usernames = []                             # list of usernames from database
        self.passwords = []                             # list of passwords from database
        self.result = None                              # result of attack
        self.usernames_file_path = usernames_file_path  # file path for usernames
        self.passwords_file_path = passwords_file_path  # file path for passwords
        self._load_database()                           # loads database

    def _load_database(self):
        try:
            self.usernames = self._decode_and_decompress(self.usernames_file_path)
            self.passwords = self._decode_and_decompress(self.passwords_file_path)
        except FileNotFoundError:
            pass

    def _decode_and_decompress(self, file_path):
        with open(file_path, "rb") as f:
            compressed_data = base64.b64decode(f.read())
            decompressed_data = gzip.decompress(compressed_data)
            return decompressed_data.decode().splitlines()

    def start_attack(self, username, password):
        # Store credentials
        self.username = username
        self.password = password

        # Start attack on thread
        attack_thread = threading.Thread(target=self._attack)
        attack_thread.start()

        # Stop thread
        attack_thread.join()

        return self.result  
    
    def _attack(self):
        # Clean up credentials input
        self._clean_credentials()

        # Search database for match
        variation_enabled = False
        success, total_matches, search_time = self._search_database(self.username, self.password)

        # If success, store results, otherwise try variations and store results
        if success:
            self.result = (success, total_matches, search_time, variation_enabled)
        else:
            # Generate varied credentials
            variation_enabled = True
            varied_usernames, varied_passwords = self._generate_varied_credentials()

            # Search database for match with each variation
            overall_success = True
            cumulative_matches = 0
            cumulative_search_time = 0.0

            for varied_username in varied_usernames:
                for varied_password in varied_passwords:
                    success, total_matches, search_time = self._search_database(varied_username, varied_password)
                    cumulative_matches += total_matches
                    cumulative_search_time += search_time
                    overall_success = overall_success and success
            
            self.result = (overall_success, cumulative_matches, cumulative_search_time, variation_enabled)
    
    def _clean_credentials(self):
        self.username = self.username.strip().lower()  
        self.password = self.password.strip()

    def _search_database(self, username, password):
        # Start time
        start_time = time.time()

        # Search usernames
        username_matches = 0
        for usr in self.usernames:
            if username in usr:
                username_matches += 1

        # Search passwords
        password_matches = 0
        for psw in self.passwords:
            if password in psw:
                password_matches += 1

        # End time
        end_time = time.time()

        # Calculate success, total matches, and search time
        success = username_matches > 0 and password_matches > 0
        total_matches = username_matches + password_matches
        search_time = end_time - start_time

        return success, total_matches, search_time

    def _generate_varied_credentials(self):
        # Define variation functions
        variations = [
            lambda x: x,
            lambda x: x + "123",
            lambda x: x.capitalize(),
            lambda x: x.upper(),
            lambda x: x + "!",
            lambda x: x.replace(".", "_"),
            lambda x: x.replace("a", "@").replace("o", "0").replace("i", "1")
        ]

        # Apply variations to username
        varied_usernames = set()
        if self.username:
            for variation in variations:
                varied_usernames.add(variation(self.username))

        # Apply variations to password
        varied_passwords = set()
        if self.password:
            for variation in variations:
                varied_passwords.add(variation(self.password))

        return list(varied_usernames), list(varied_passwords)
