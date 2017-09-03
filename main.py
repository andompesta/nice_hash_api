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
    parser.add_argument("--api_id", type=str, default="ID418401", help="account id of nicehas")
    parser.add_argument("--api_key", type=str, default="fcd84015-68a4-3f97-0e0d-1f5f35e2470b",
                        help="api key of nicehas")

    return parser.parse_args()




if __name__ == '__main__':
    args = __pars_args__()
    db = client[args.database_name]

    get_personal_orders(args.base_url, "SHA256", args.api_id, args.api_key, collection=db['PersonalOrders'])
