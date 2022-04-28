import pickle
from multiprocessing.connection import Listener, Client
from typing import Tuple


class ServerNetwork:
    def deploy_server(self, address: Tuple[str, int] = ("192.168.40.10", 8080)):
        if len(address) != 2:
            return None
        with Listener(address) as listener:
            response = None
            while not response:
                request = None
                while not request:
                    with listener.accept() as conn:
                        request = conn.recv_bytes()
                        print(request)
                client_address = pickle.loads(request)["client_address"]
                option = pickle.loads(request)["option"]

                self.handler(option)

                response = request
                if response:
                    try:
                        with Client(client_address) as conn:
                            conn.send_bytes(response)
                    except ConnectionRefusedError as e:
                        print(e)
                    else:
                        response = None

    # TODO change response on api
    @staticmethod
    def handler(option: int) -> bool:
        if option is None:
            return False
        if option == 1:
            response = 123
            pass
        elif option == 2:
            pass
        else:
            pass
