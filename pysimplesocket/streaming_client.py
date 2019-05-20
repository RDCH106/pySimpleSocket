# -*- coding: utf-8 -*-

import socket
import time
import sys
import argparse
try:
    from pysimplesocket.abstract_client import AbstractClient, Metadata
except ModuleNotFoundError as e:
    from abstract_client import AbstractClient, Metadata


class StreamingClient(AbstractClient):

    meta = Metadata(version='0.0.2', author='Rubén de Celis Hernández')

    def __init__(self, ip=None, port=None):
        self.__ip = ip
        self.__port = port
        # self.__receiver_thread = None
        # self.__stop = False
        self.__socket_family = socket.AF_INET
        self.__socket_type = socket.SOCK_STREAM
        super(StreamingClient, self).__init__()

    def receiver_worker(self):
        try:
            # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
            client = socket.socket(self.__socket_family, self.__socket_type)

            # connect the client
            client.connect((self.__ip, self.__port))
            print('Socket opened')

            # while not self.__stop:
            while not self.v_stop:
                # receive the response data (4096 is recommended buffer size)
                response = client.recv(4096)

                if len(response) > 0:
                    print(response)

        except ConnectionRefusedError as e:
            print(str(e))
        except ConnectionResetError as e:
            print(str(e))
        except Exception as e:
            print(e)
        finally:
            client.close()
            print('Socket closed')

    def run(self):
        super(StreamingClient, self).run()
        # if self.__receiver_thread is None:
        #     self.__stop = False
        #
        #     self.__receiver_thread = threading.Thread(target=self.receiver_worker)
        #     self.__receiver_thread.daemon = True
        #     self.__receiver_thread.start()

    def stop(self):
        super(StreamingClient, self).stop()
        # self.__receiver_thread = None
        # self.__stop = True


if __name__ == "__main__":

    # Parse arguments provided
    parser = argparse.ArgumentParser()
    # meta = Metadata()
    # parser.add_argument('-v', '--version', action='version', version=meta.get_version())
    parser.add_argument('-v', '--version', action='version', version=StreamingClient.meta.get_version())
    parser.add_argument('-s', '--host', dest='host', help='Host server to connect', default=None, required=True)
    parser.add_argument('-p', '--port', dest='port', help='Port to connect', default=None, required=True)

    args = parser.parse_args()

    receiver = StreamingClient(args.host, int(args.port))
    receiver.run()

    while True:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            receiver.stop()
            time.sleep(1)
            sys.exit()
