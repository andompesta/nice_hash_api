import os
import sys
import argparse
from pymongo import MongoClient
from functools import partial
import logging
import logging.config
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

from rest_full_api.api_public_lib import *
from rest_full_api.db_lib import *
from rest_full_api.api_helper import wrapper_function


def __pars_args__():
    parser = argparse.ArgumentParser(description='nice_hash_client')
    parser.add_argument('--base_url', type=str, default="https://api.nicehash.com/api", help="base nice_hash_url")
    parser.add_argument("-db_name", "--database_name", type=str, default="NiceHash", help="name of the db where to save all the info")
    parser.add_argument("--api_id", type=str, default="418401", help="account id of nicehas")
    parser.add_argument("--api_key", type=str, default="fcd84015-68a4-3f97-0e0d-1f5f35e2470b", help="api key of nicehas")
    parser.add_argument("-lf", "--logging_file", type=str, default=None, help="logging file")

    return parser.parse_args()




if __name__ == '__main__':
    args = __pars_args__()
    # create logger
    logger = logging.getLogger('my_logger')
    if args.logging_file:
        fh = logging.FileHandler(args.logging_file)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(filename)s:%(lineno)s - %(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logging.getLogger('requests').addHandler(fh)

    client = MongoClient('localhost', 27017)
    db = client[args.database_name]

    try:
        logger.info("start process with pid: {}".format(os.getpid()))
        while True:
            time = datetime.now()
            logger.info(time.strftime("%Y-%m-%d %H:%M:%S"))
            while wrapper_function(partial(get_global_current,
                                           base_url=args.base_url,
                                           collection=db['GlobalCurrentStatus'],
                                           time=time)):
                continue
            # get_global_24(args.base_url, collection=db['Global24Status'])
            sleep(3)
            # for key, value in alg_table.items():
            #     get_orders_by_algo(args.base_url, collection=db['Order{}'.format(value)], algo="{}".format(value), location=0, time=time)
            # sleep(3)
            while wrapper_function(partial(get_buy_info,
                                           base_url=args.base_url,
                                           collection=db['BuyInfo'],
                                           time=time)):
                continue
            
            sleep_time = 30 - (datetime.now() - time).seconds
            if sleep_time > 0:
                sleep(sleep_time)
    except Exception as e:
        logger.error(e)
    finally:
        logger.info("End the pocess: {}".format(os.getpid()))

