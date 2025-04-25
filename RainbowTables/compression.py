import gzip
import base64

def encode_and_compress(input_path, output_path):
    # Read plain text file
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read().encode("utf-8")

    # Compress with gzip
    compressed = gzip.compress(text)

    # Encode with base64
    encoded = base64.b64encode(compressed)

    # Write to output file (binary)
    with open(output_path, "wb") as f:
        f.write(encoded)

def decode_and_decompress(file_path):
    with open(file_path, "rb") as f:
        compressed_data = base64.b64decode(f.read())
        decompressed_data = gzip.decompress(compressed_data)
        return decompressed_data.decode("utf-8").splitlines()
    
def save_compressed_table_from_file(input_path, output_path):
    # Read plain text file
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read().encode("utf-8")
    
    # Compress with gzip and save
    with gzip.open(output_path, "wb") as f:
        f.write(text)

# Example usage
# encode_and_compress("sha1_table_1m_1000.txt", "sha1-rainbow-short.rt")