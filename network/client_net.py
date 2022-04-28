import pickle

from multiprocessing.connection import Client, Listener
from typing import Tuple, Union, Any

from network import util
from network.seting import END_BYTES, PORT


class ClientNetwork:
    def __init__(self):
        self.package = {
            "client_address": tuple,
            "option": int,
            "data": str
        }

    # TODO wait time
    def send_package(self, node_address: Tuple[str, int], pack: dict) -> bool or dict:
        # client == me
        pack["client_address"] = (util.get_ip(), PORT)
        with Client(node_address) as conn:
            conn.send_bytes(pickle.dumps(pack) + END_BYTES)
        res = self.read_package(pack["client_address"])
        return res

    # TODO buffer size and max size
    @staticmethod
    def read_package(my_address: tuple) -> Union[bool, dict]:
        while True:
            with Listener(my_address) as listener:
                with listener.accept() as conn:
                    try:
                        response = conn.recv_bytes()
                        if END_BYTES in response:
                            response = response.split(END_BYTES)[0]
                            return pickle.loads(response)
                        else:
                            raise Exception("[-] END_BYTES not found.")
                    except EOFError:
                        return False
