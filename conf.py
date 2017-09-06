import logging
from bidict import bidict
from functools import partial

logger = None
class Singleton:
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Logger:
    __metaclass__ = Singleton
    def __init__(self, filename, logging_level):
        if filename:
            logging.basicConfig(filename="console.log",level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s')

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def error(self, msg):
        logging.error(msg)

    def warn(self, msg):
        logging.warning(msg)


def create_logger(filename=None, logging_level=logging.DEBUG):
    global logger
    logger = Logger(filename=filename, logging_level=logging_level)
    return logger
alg_table = bidict({
    0: "Scrypt",
    1: "SHA256",
    2: "ScryptNf",
    3: "X11",
    4: "X13",
    5: "Keccak",
    6: "X15",
    7: "Nist5",
    8: "NeoScrypt",
    9: "Lyra2RE",
    10: "WhirlpoolX",
    11: "Qubit",
    12: "Quark",
    13: "Axiom",
    14: "Lyra2REv2",
    15: "ScryptJaneNf16",
    16: "Blake256r8",
    17: "Blake256r14",
    18: "Blake256r8vnl",
    19: "Hodl",
    20: "DaggerHashimoto",
    21: "Decred",
    22: "CryptoNight",
    23: "Lbry",
    24: "Equihash",
    25: "Pascal",
    26: "X11Gost",
    27: "Sia",
    28: "Blake2s",
    29: "Skunk"
})