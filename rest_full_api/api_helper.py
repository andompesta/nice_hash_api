import logging
from time import sleep
logger = logging.getLogger('my_logger')

def wrapper_function(fn, sleep_time=12):
    '''
    execute function in save way
    :param fn: function to call
    :param sleep_time: time to sleep
    :return: 
    '''
    try:
        return fn()
    except Exception as e:
        logger.error(e)
        sleep(sleep_time)
        return True

def as_float(obj):
    """Checks each dict passed to this function if it contains the key "value"
    Args:
        obj (dict): The object to decode

    Returns:
        dict: The new dictionary with changes if necessary
    """
    for i, value in obj.items():
        if isinstance(value, str):
            try:
                obj[i] = float(value)
            except ValueError:
                pass
    return obj