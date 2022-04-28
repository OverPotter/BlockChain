import base64
import pickle
import sqlite3
import time

from data_chain import DataChain
from crypto import Crypto
from settings import *


class Chain(Crypto, DataChain):
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(DB_FILENAME)
        self.chain = self.conn.cursor()

    # TODO exception
    def new_chain(self, receiver: str) -> bool or Exception:
        try:
            self.chain.execute(
                "CREATE TABLE `BlockChain` (`Id` INTEGER PRIMARY KEY AUTOINCREMENT,`Hash` VARCHAR(44) UNIQUE,`Block` TEXT);")
        except sqlite3.OperationalError:
            pass
        finally:
            genesis = self.block
            genesis.update({
                "PreviousHash": self.hash_sha256(GENESIS_BLOCK),
                "Miner": receiver,
                "TimeStamp": "%.20f" % time.time()
            })
            genesis["Mapping"].append({
                STORAGE_CHAIN: STORAGE_VALUE,
                receiver: GENESIS_REWARD
            })
            genesis["CurrentHash"] = self.hash_sha256(genesis)
            self.add_block_to_chain(genesis)
            return True

    def add_block_to_chain(self, block: dict):
        self.chain.execute(
            "INSERT INTO `BlockChain` (`Hash`, `Block`) VALUES (?, ?)",
            (base64.b64encode(block["CurrentHash"]),
             pickle.dumps(block))
        )
        return self.conn.commit()

    def get_balance(self, address, block_count):
        self.chain.execute(
            "SELECT `Block` FROM `BlockChain` WHERE Id <= (?) ORDER BY Id DESC",
            block_count
        )
        # todo choose .fetchall()[0][0]

    def get_chain_size(self):
        block_count = self.chain.execute(
            "SELECT `Id` FROM `BlockChain` ORDER BY `Id` DESC"
        )
        return block_count.fetchall()[0][0]

    def add_balance(self):
        pass

    def get_last_hash(self):
        pass


if __name__ == '__main__':
    c = Chain()
    c.new_chain("receiver")
