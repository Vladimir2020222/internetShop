import os

SECRET_KEY = "Ji9N61GjbgTvdwjjCfdugcXFXXoID7OHdL9XbfQN5SbzZs+l5ke3miCTFzm5SXmtD26ybuylpF6HOgs+jjE2pIqUYZrdTTn6iWusZ3POkQyqmKdxwm4XUWO7Vkz2IdqUPegP3Mn3vxiGoDWOlRc+diGnnwYsijhbuv0em3VwrJCtKh7CczrsqBnwwH3MsmC35BWRBi9FUuldQ01"

DB_USERNAME = os.environ.get("DB_USERNAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

ENCODE_JWT_ALGORITHM = "HS256"
DECODE_JWT_ALGORITHMS = ["HS256"]
