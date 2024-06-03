import uuid

def generate_random_file_name():
    return f"{uuid.uuid4}"

uuid_filename = generate_random_file_name()