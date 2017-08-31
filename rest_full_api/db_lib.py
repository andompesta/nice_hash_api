from datetime import datetime
from conf import logger

def pprint_hostory_orders(history_orders):
    for history_order in history_orders:
        logger.info("Time: {}".format(history_order['time']))
        logger.info("limit_speed\t\talive\t\tprice\t\tid\t\ttype\t\tworkers\t\taccepted_speed")
        for order in history_order['orders']:
            logger.info("\t{}\t\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(order["limit_speed"],
                                                          order["alive"],
                                                          order["price"],
                                                          order["id"],
                                                          order["type"],
                                                          order["workers"],
                                                          order["accepted_speed"]))


def get_histrory_orders(collection, limit=1):
    history_orders = collection.find().sort([('time', -1)]).limit(limit)
    return history_orders

def get_global_current_status_by_algo(collection, algo, limit=100):
    '''
    Return the last limit global state of a give algorithm, sorted by time
    :param collection: collection from which read the data
    :param algo: algorithm selected
    :param limit: number of timestemp to return
    :return:
    '''
    return collection.aggregate([{"$project":
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