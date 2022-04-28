from typing import Any

from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
import os
import pickle

transaction = {
    "RandBytes": bytes,
    "PreviousBlock": bytes,
    "Sender": str,
    "Receiver": str,
    "Value": int,
    "ToStorage": int,
    "CurrentHash": bytes,
    "Signature": bytes
}


class Crypto:
    def __init__(self):
        pass

    @staticmethod
    def hash_sha256(data: Any) -> bytes:
        hashed_object = SHA256.new(pickle.dumps(data)).hexdigest()
        return hashed_object.encode()

    @staticmethod
    def generate_keys():
        private_key = RSA.generate(2048, randfunc=os.urandom)
        public_key = private_key.publickey()
        return private_key.export_key("DER"), public_key.export_key("DER")

    @staticmethod
    def sign_data(data: dict, pr_key):
        data_hash = SHA256.new(pickle.dumps(data))
        signature = pkcs1_15.new(RSA.import_key(pr_key)).sign(data_hash)
        return signature

    @staticmethod
    def verify(data: dict, pub_key, signature) -> bool:
        try:
            data_hash = SHA256.new(pickle.dumps(data))
            pkcs1_15.new(RSA.import_key(pub_key)).verify(data_hash, signature)
        except ValueError:
            return False
        else:
            return True


# if __name__ == '__main__':
#     c = Crypto()
#     pr_key, pub_key = c.generate_keys()
#     signature = c.sign_data(transaction, pr_key)
#     # transaction.update({"1": 1})
#     c.verify(transaction, pub_key,
#
#              signature)
#     print(pr_key)
#     print(pub_key)
# pip install pycryptodomex
