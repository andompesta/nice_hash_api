import requests
import json
from datetime import datetime
from conf import logger, alg_table
from pymongo import ReturnDocument
from rest_full_api.api_helper import as_float
from time import sleep

def get_version(base_url):
    response = requests.get(base_url)
    if response.ok:
        data = json.loads(response.content)
        logger.info("status of the request \n version:{}\n methods:{}".format(data['result']['api_version'], data['method']))
    else:
        #error
        response.raise_for_status()


def get_global_current(base_url, collection, location=0, time=None):
    '''
    Get current profitability (price) and hashing speed for all algorithms. Refreshed every 30 seconds.
    :param base_url: base url of nicehash's api
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash)
    :param collection: collection where save the data
    :return:
    '''
    params = {'location': location}
    url = "{}?method=stats.global.current".format(base_url)
    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        data = data['result']
        if time:
            data['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for stat in data['stats']:
            stat['algo'] = alg_table[stat['algo']]

        try:
            curr_state_id = collection.insert_one(data)
            logger.debug("inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e
    elif response.status_code == 404:
        # error is caused by nice-hash
        sleep(3)
        get_global_current(base_url, collection, location, time)
        logger.warn("get_global_current\turl: {}\treason: {}\tstatus_code:{}".format(response.url, response.reason, response.status_code))
    else:
        #error
        response.raise_for_status()


def get_global_24(base_url, collection):
    '''
    Get average profitability (price) and hashing speed for all algorithms in past 24 hours.
    :param base_url: base url of nicehash's api
    :param collection: where to save the info in the db
    :return:
    '''
    url = "{}?method=stats.global.24h".format(base_url)
    response = requests.get(url)
    if response.ok:
        today = datetime.now()
        data = json.loads(response.content, object_hook=as_float)
        data = data['result']
        data['time'] = "{}-{}-{}".format(today.year, today.month, today.day)
        for stat in data['stats']:
            stat['algo'] = alg_table[stat['algo']]

        try:
            curr_state_id = collection.insert_one(data)
            logger.debug(
                "inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e
    else:
        # error
        response.raise_for_status()

def get_orders_by_algo(base_url, collection, algo, location=0, time=None):
    '''
    Get all orders for certain algorithm. Refreshed every 30 seconds.
    :param base_url: base url of nicehash's api
    :param collection: where to save the info in the db
    :param algo: name of the algorithm to check
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash)
    :return:
    '''
    params = {'algo': alg_table.inv[algo],
              'location': location}

    url = "{}?method=orders.get".format(base_url)
    response = requests.get(url, params=params)

    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        data = data['result']
        if time:
            data['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            curr_state_id = collection.insert_one(data)
            logger.debug(
                "inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e
    else:
        # error
        response.raise_for_status()


def get_buy_info(base_url, collection, time=None):
    '''
    Get needed information for buying hashing power using.
    :param base_url: base url of nicehash's api
    :param collection: where to save the info in the db
    '''

    url = "{}?method=buy.info".format(base_url)
    response = requests.get(url)

    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        data = data['result']
        if time:
            data['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            curr_state_id = collection.insert_one(data)
            # update_doc = collection.find_one_and_update({}, {'$set': {'algorithms': data['algorithms'],
            #                                              'time': data['time'],
            #                                              'down_time': data['down_time'],
            #                                              'static_fee': data['static_fee'],
            #                                              'min_amount': data['min_amount'],
            #                                              'dynamic_fee': data['dynamic_fee']
            #                                              }
            #                                     },
            #                                return_document=ReturnDocument.AFTER)
            logger.debug(
                "inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e
    elif response.status_code == 404:
        # error is caused by nice-hash
        sleep(3)
        get_buy_info(base_url, collection, time)
        logger.warn("get_buy_info\turl: {}\treason: {}\tstatus_code:{}".format(response.url, response.reason, response.status_code))
    else:
        # error
        response.raise_for_status()