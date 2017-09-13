import requests
import json
from datetime import datetime
from conf import alg_table
from rest_full_api.api_helper import as_float
from pymongo import ReturnDocument
from rest_full_api.db_lib import __format_balance_cursor__
import logging
logger = logging.getLogger("my_logger")


def orders_get(base_url, algo, api_id, api_key, collection, location=0):
    '''
    Get all orders for certain algorithm owned by the customer. Refreshed every 30 seconds.
    :param base_url:base url of nicehash's api
    :param algo: name of the algorithm
    :param api_id: api_id
    :param api_key: api_key
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash)
    :return:
    '''
    url = "{}?method=orders.get&my".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "algo": alg_table.inv[algo],
              "location": location}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        data = data['result']
        data['algo'] = algo
        data['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            curr_state_id = collection.insert_one(data)
            logger.debug(
                "inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e
        return data
    else:
        # error
        response.raise_for_status()

def orders_create(base_url, algo, amount, price, pool_host, pool_port, pool_user, pool_pass, api_id, api_key, limit=0, location=0):
    '''
    Create new order. Refer to order creation page for details. Only standard orders can be created with use of API.
    :param base_url: base url of nicehash's api
    :param algo: Algorithm name.
    :param amount: Pay amount in BTC.
    :param price: Price in BTC/GH/Day or BTC/TH/Day.
    :param limit: Speed limit in GH/s or TH/s (0 for no limit).
    :param pool_host: Pool hostname or IP.
    :param pool_port: Pool port.
    :param pool_user: Pool username.
    :param pool_pass: Pool password.
    :param api_id: API ID.
    :param api_key: API Key.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    '''
    url = "{}?method=orders.create".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "algo": alg_table.inv[algo],
              "amount": amount,
              "price": price,
              "limit": limit,
              "pool_host": pool_host,
              "pool_port": pool_port,
              "pool_user": pool_user,
              "pool_pass": pool_pass,
              "location": location}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()


def orders_refill(base_url, algo, order_id, amount, api_id, api_key, location=0):
    '''
    Refill order with extra Bitcoins, which essentially extends the running time of an order.
    You can refill your orders as many times as you want. 
    The 0.0001 BTC non-refundable order submission fee is not charged when you refill your order.
    :param base_url: base url of nicehash's api
    :param algo: Algorithm name
    :param order_id: Order ID.
    :param amount: Refill amount in BTC.
    :param api_id: API ID.
    :param api_key: API Key.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    '''
    url = "{}?method=orders.refill".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "location": location,
              "algo": alg_table.inv[algo],
              "order": order_id,
              "amount": amount}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()

def orders_remove(base_url, algo, order_id, api_id, api_key, location=0):
    """
    Remove existing order.
    :param base_url: base url of nicehash's api
    :param algo: Algorithm marked with name.
    :param order_id: Order ID.
    :param api_id: API ID.
    :param api_key: API Key.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    """
    url = "{}?method=orders.remove".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "location": location,
              "algo": alg_table.inv[algo],
              "order": order_id}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()

def orders_set_price(base_url, algo, order_id, price, api_id, api_key, location=0):
    """
    Set new price for the existing order. Only increase is possible.
    :param base_url: base url of nicehash's api
    :param algo: Algorithm marked with name.
    :param order_id:  Order ID.
    :param price: Price in BTC/GH/Day or BTC/TH/Day.
    :param api_id: API ID.
    :param api_key: API KEY.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    """
    url = "{}?method=orders.set.price".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "location": location,
              "algo": alg_table.inv[algo],
              "order": order_id,
              "price": price}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()

def orders_set_price_decrease(base_url, algo, order_id, api_id, api_key, location=0):
    """
    Decrease price for the existing order. Price decrease possible every 10 minutes. Read FAQ for more information.
    To avoid manipulation, price decrease is only available within predefined price steps, can be applied only each 
    10 minutes and resets your position to the bottom of sub-list of same-priced orders.
    :param base_url: base url of nicehash's api
    :param algo_id: Algorithm marked with name.
    :param order_id: Order ID.
    :param api_id: API ID.
    :param api_key: API KEY.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    """
    url = "{}?method=orders.set.price.decrease".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "location": location,
              "algo": alg_table.inv[algo],
              "order": order_id}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()

def orders_set_limit(base_url, algo, order_id, liimit, api_id, api_key, location=0):
    """
    Set new limit for the existing order.
    :param base_url: base url of nicehash's api
    :param algo: Algorithm marked with name.
    :param order_id: Order ID.
    :param liimit: Speed limit in GH/s or TH/s (0 for no limit).
    :param api_id: API ID.
    :param api_key: API KEY.
    :param location: 0 for Europe (NiceHash), 1 for USA (WestHash).
    :return: 
    """
    url = "{}?method=orders.set.limit".format(base_url)
    params = {"id": api_id,
              "key": api_key,
              "location": location,
              "algo": alg_table.inv[algo],
              "order": order_id,
              "limit": liimit}

    response = requests.get(url, params=params)
    if response.ok:
        data = json.loads(response.content, object_hook=as_float)
        logger.info(data["result"]["success"])
    else:
        # error
        response.raise_for_status()

def balance(base_url, api_id, api_key, collection, time=None):
    """
    Get current confirmed Bitcoin balance.
    :param base_url: base url of nicehash's api
    :param api_id: API ID.
    :param api_key: API Key or ReadOnly API Key.
    :return: 
    """
    url = "{}?method=balance".format(base_url)
    params = {"id": api_id,
              "key": api_key}

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
            logger.debug("inserted document_id:{} \tin collection:{}".format(curr_state_id, collection._Collection__name))
        except Exception as e:
            logger.error("error in inserting doc: {}".format(data))
            raise e

        return __format_balance_cursor__([data])
    else:
        # error
        response.raise_for_status()