import binascii
import os


def generate_token():
    """Generate and return a random token"""
    return binascii.hexlify(os.urandom(20)).decode()
