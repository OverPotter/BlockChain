import os
from typing import List

from settings import *
from crypto import Crypto
from user import User
from chain import Chain


class Block(User, Chain):
    def __init__(self):
        super().__init__()

        # self.block = {
        #     "Nonce": int,
        #     "Difficult": int,
        #     "CurrentHash": bytes,
        #     "PreviousHash": bytes,
        #     "Transaction": List[dict],
        #     "Mapping": List[dict],
        #     "Miner": str,
        #     "Signature": bytes,
        #     "TimeStamp": str
        # }
        # self.transaction = {
        #     "RandBytes": bytes,
        #     "PreviousBlock": bytes,
        #     "Sender": str,
        #     "Receiver": str,
        #     "Value": int,
        #     "ToStorage": int,
        #     "CurrentHash": bytes,
        #     "Signature": bytes
        # }

    def new_block(self, miner: str, prev_hash: bytes) -> dict:
        block = self.block
        block.update({
            "Difficult": DIFFICULTY,
            "PreviousBlock": prev_hash,
            "Miner": miner,
        })
        return block

    def new_transaction(self, last_hash: bytes, receiver: str, value: int) -> dict:
        transaction = self.transaction
        transaction.update({
            "RandBytes": os.urandom(RANDOM_BYTES),
            "PreviousBlock": last_hash,
            "Sender": self.user_address,
            "Receiver": receiver,
            "Value": value,
        })
        if value > START_PERCENT:
            transaction["ToStorage"] = STORAGE_REWARD
        transaction["CurrentHash"] = self.hash_sha256(transaction)
        transaction["Signature"] = self.sign_data(transaction, self.private_key)
        return transaction

    # TODO block ?
    def add_transaction(self, block: dict, transaction: dict) -> bool or Exception:
        if transaction["Value"] == 0:
            raise Exception("[-] add_transaction error: Transaction Value = 0")
        if transaction["Sender"] != STORAGE_CHAIN and len(block["Transaction"]) == TXS_LIMIT:
            raise Exception("[-] add_transaction error: Transaction limit")
        if transaction["Sender"] != STORAGE_CHAIN and transaction["Value"] > START_PERCENT and \
                transaction["ToStorage"] != STORAGE_REWARD:
            raise Exception("[-] add_transaction error: Storage reward not passed")
        # TODO get
        if transaction["PreviousBlock"] != self.chain.get_last_hash():
            raise Exception("[-] add_transaction error: The hashes didn't match")

        # TODO Mapping ?
        balance_in_transaction = transaction["Value"] + transaction["ToStorage"]
        balance_in_chain = None
        sender = transaction["Sender"]
        for m in block["Mapping"]:
            if sender in m.keys():
                balance_in_chain = m[sender]
                break
        if balance_in_chain is None:
            balance_in_chain = self.chain.get_balance()

        if balance_in_transaction > balance_in_chain:
            raise Exception("[-] add_transaction error: Insufficient funds")

        for m in block["Mapping"]:
            if sender in m.keys():
                m[sender] = balance_in_chain - balance_in_transaction
        # todo get
        self.chain.add_balance()
        self.chain.add_balance()
        block["Transaction"].append(transaction)
        return True


if __name__ == '__main__':
    b = Block()
    b.new_chain('qwe')
    print(b.new_transaction(b'kkkkk', 'qwerty', 5))
