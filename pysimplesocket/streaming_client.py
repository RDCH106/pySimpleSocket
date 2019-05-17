# -*- coding: utf-8 -*-

import socket
import threading
import time
import sys


class StreamingClient(object):
    def __init__(self, ip=None, port=None):
        self.__ip = ip
        self.__port = port
        self.__receiver_thread = None
        self.__stop = False

    def receiver_worker(self):
        try:
            # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # connect the client
            client.connect((self.__ip, self.__port))
            print('Socket opened')

            while not self.__stop:
                # receive the response data (4096 is recommended buffer size)
                response = client.recv(4096)

                if len(response) > 0:
                    print(response)

        except ConnectionRefusedError as e:
            print(e)
        finally:
            client.close()
            print('Socket closed')

    def run(self):
        if self.__receiver_thread is None:
            self.__stop = False

            self.__receiver_thread = threading.Thread(target=self.receiver_worker)
            self.__receiver_thread.daemon = True
            self.__receiver_thread.start()

    def stop(self):
        self.__receiver_thread = None
        self.__stop = True


if __name__ == "__main__":
    receiver = StreamingClient("127.0.0.1", 50043)
    receiver.run()

    while True:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            receiver.stop()
            sys.exit()
