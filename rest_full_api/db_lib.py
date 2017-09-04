from datetime import datetime
from conf import logger
import pandas as pd

def __format_balance_cursor__(query_cursor):
    ret = {}
    for balance in query_cursor:
        time = balance["time"]
        del balance["time"]
        ret[datetime.strptime(time, "%Y-%m-%d %H:%M:%S")] = balance

    return pd.DataFrame.from_dict(ret, orient="index")


def __format_status_cursor__(query_cursor, algos):
    '''
    format the cursor of retrieved global status
    :param query_cursor: cursor to the query results
    :param algos: list of algorithms to return
    :return: dictiorany of pandas timeframe
    '''
    pa_dict = {}
    for algo in algos:
        pa_dict[algo] = {}

    for obj in query_cursor:
        for stat in obj["stats"]:
            algo = stat["algo"]
            del stat["algo"]
            pa_dict[algo][datetime.strptime(obj["time"], "%Y-%m-%d %H:%M:%S")] = stat

    return {algo: pd.DataFrame.from_dict(pa_dict[algo], orient="index") for algo in algos}

def __format_history_orders__(history_orders_cursor):
    '''
    format the cursor of the retrieved history orders on ne algorithm
    :param history_orders_cursor: cursor to transform
    :return: DataFrame
    '''
    ret = {}
    for history_order in history_orders_cursor:
        ret[datetime.strptime(history_order["time"], "%Y-%m-%d %H:%M:%S")] = history_order["orders"]
    return pd.DataFrame.from_dict(ret, orient="columns")


def pprint_hostory_orders(history_orders):
    for history_order in history_orders:
        logger.info("Time: {}".format(history_order))
        logger.info("limit_speed\t\talive\t\tprice\t\tid\t\ttype\t\tworkers\t\taccepted_speed")
        for order in history_orders[history_order]:
            logger.info("\t{}\t\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(order["limit_speed"],
                                                          order["alive"],
                                                          order["price"],
                                                          order["id"],
                                                          order["type"],
                                                          order["workers"],
                                                          order["accepted_speed"]))


def get_histrory_orders(collection, limit=1):
    history_orders = collection.find().sort([('time', -1)]).limit(limit)
    return __format_history_orders__(history_orders)

def get_global_current_status_by_algo(collection, algo, limit=100):
    '''
    Return the last limit global state of a give algorithm, sorted by time
    :param collection: collection from which read the data
    :param algo: algorithm selected
    :param limit: number of timestemp to return
    :return:
    '''
    query_cursor = collection.aggregate([{"$project":
        {"stats":
            {"$filter":
                {"input": "$stats",
                 "as": "stat",
                 "cond": {"$eq": ["$$stat.algo", algo]}
                }
            },
         "time": 1
        }
    },
                          {"$sort": {"time": 1}},
                          {"$limit": limit}])

    return __format_status_cursor__(query_cursor, [algo])



def get_multi_global_current_status_by_algo(collection, algos, limit=100):
    '''
    Return the last limit global state of a give algorithm, sorted by time
    :param collection: collection from which read the data
    :param algos: list of algorithm selected
    :param limit: number of timestemp to return
    :return:
    '''
    query = [{"$eq": ["$$stat.algo", algo]} for algo in algos]

    query_cursor = collection.aggregate([{"$project":
        {"stats":
            {"$filter":
                {"input": "$stats",
                 "as": "stat",
                 "cond": {"$or": query}
                }
            },
         "time": 1
        }
    },
                          {"$sort": {"time": 1}},
                          {"$limit": limit}])

    return __format_status_cursor__(query_cursor, algos)


def get_balance(collection, limit=100):
    '''
    Return the last limit balance
    :param collection: collection from which read the data
    :param limit: number of timestemp to return
    :return:
    '''
    query_cursor = collection.find().sort([('time', -1)]).limit(limit)
    return __format_balance_cursor__(query_cursor)