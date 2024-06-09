import uuid
import secrets

def generate_random_file_name():
    return secrets.token_hex(16)

uuid_filename = generate_random_file_name()