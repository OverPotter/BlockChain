class DataChain:
    def __init__(self):
        self.block = {
            "Nonce": int,
            "Difficult": int,
            "CurrentHash": bytes,
            "PreviousHash": bytes,
            "Transaction": list,
            "Mapping": list,
            "Miner": str,
            "Signature": bytes,
            "TimeStamp": str
        }
        self.transaction = {
            "RandBytes": bytes,
            "PreviousBlock": bytes,
            "Sender": str,
            "Receiver": str,
            "Value": int,
            "ToStorage": int,
            "CurrentHash": bytes,
            "Signature": bytes
        }