from crypto import Crypto


class User:
    def __init__(self):
        self.private_key, self.user_address = Crypto().generate_keys()
