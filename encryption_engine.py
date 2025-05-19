
# encryption_engine.py

def encrypt_bhava_vectors(vectors):
    return [[v ^ 42 for v in vec] for vec in vectors]  # XOR mock

def decrypt_bhava_vectors(data):
    return [[v ^ 42 for v in vec] for vec in data]  # XOR mock
