# -*- coding: utf-8 -*-

import threading
from abc import ABC, abstractmethod  # Python 3.4+


class Metadata:
    def __init__(self, version, author):
        self.__version__ = version
        self.__author__ = author

    def get_version(self):
        return self.__version__

    def get_author(self):
        return self.__author__


class AbstractClient(ABC):

    def __init__(self):
        self.__receiver_thread = None
        self.__stop = False

    @property
    def v_stop(self):
        return self.__stop

    @abstractmethod
    def receiver_worker(self):
        pass

    def run(self):
        if self.__receiver_thread is None:
            self.__stop = False

            self.__receiver_thread = threading.Thread(target=self.receiver_worker)
            self.__receiver_thread.daemon = True
            self.__receiver_thread.start()

    def stop(self):
        self.__receiver_thread = None
        self.__stop = True
