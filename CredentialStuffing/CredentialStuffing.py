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
        success, total_matches, search_time = self._search_database()

        # Return results if success
        if success:
            self.result = (success, total_matches, search_time)
        else:
            # TODO Generate varied credentials
            # TODO Search against database
            # if (hit found): self.result = stats crack success
            # else: self.result = crack failed
            pass

    def _clean_credentials(self):
        self.username = self.username.strip().lower()  
        self.password = self.password.strip()

    def _search_database(self):
        # Start time
        start_time = time.time()

        # Search usernames
        username_matches = 0
        for username in self.usernames:
            if self.username in username:
                username_matches += 1

        # Search passwords
        password_matches = 0
        for password in self.passwords:
            if self.password in password:
                password_matches += 1

        # End time
        end_time = time.time()

        # Calculate success, total matches, and search time
        success = username_matches > 0 and password_matches > 0
        total_matches = username_matches + password_matches
        search_time = end_time - start_time

        return success, total_matches, search_time

    def generate_varied_credentials(self):
        pass
