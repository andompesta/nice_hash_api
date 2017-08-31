import argparse
from rest_full_api.api_lib import *
from rest_full_api.db_lib import *
from rest_full_api.plot_lib import *

from pymongo import MongoClient

client = MongoClient('localhost', 27017)


def __pars_args__():
    parser = argparse.ArgumentParser(description='nice_hash_client')
    parser.add_argument('--base_url', type=str, default="https://api.nicehash.com/api", help="base nice_hash_url")
    parser.add_argument("-db_name","--database_name", type=str, default="NiceHash", help="name of the db where to save all the info")

    return parser.parse_args()




if __name__ == '__main__':
    args = __pars_args__()
    db = client[args.database_name]



    get_version(args.base_url)
    get_global_current(args.base_url, collection=db['GlobalCurrentStatus'])
    get_global_24(args.base_url, collection=db['Global24Status'])
    get_orders_by_algo(args.base_url, collection=db['OrderSHA256'], algo="SHA256", location=0)
    get_buy_info(args.base_url, collection=db['BuyInfo'])
    histrory_orders = get_histrory_orders(db['OrderSHA256'], limit=2)
    pprint_hostory_orders(histrory_orders)

    history_current_status = get_global_current_status_by_algo(db['GlobalCurrentStatus'], algo="SHA256")
    plot_global_current_state(history_current_status)