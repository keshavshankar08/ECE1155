import gzip
import base64

def compress_and_encode(input_file, output_file):
    with open(input_file, "rb") as f:
        compressed_data = gzip.compress(f.read())
        encoded_data = base64.b64encode(compressed_data)

    with open(output_file, "wb") as f:
        f.write(encoded_data)

def decode_and_decompress(input_file, output_file):
    with open(input_file, "rb") as f:
        encoded_data = f.read()
        compressed_data = base64.b64decode(encoded_data)
        original_data = gzip.decompress(compressed_data)

    with open(output_file, "wb") as f:
        f.write(original_data)

# Compress and encode the files
#compress_and_encode("CredentialStuffing/usernames.txt", "CredentialStuffing/usernames.gz.b64")
compress_and_encode("CredentialStuffing/passwords.txt", "CredentialStuffing/passwords.gz.b64")

# Decode and decompress the files
#decode_and_decompress("CredentialStuffing/usernames.gz.b64", "CredentialStuffing/usernames.txt")
#decode_and_decompress("CredentialStuffing/passwords.gz.b64", "CredentialStuffing/passwords.txt")
