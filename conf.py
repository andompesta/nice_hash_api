import logging
from bidict import bidict

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.
    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.
    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.
    Limitations: The decorated class cannot be inherited from.
    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.
        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def info(self, msg):
        logging.info(msg)

    def debug(self, msg):
        logging.debug(msg)

    def error(self, msg):
        logging.error(msg)


logger = Logger.instance()

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