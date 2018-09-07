from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re
import threading

"""
Transaction class for containing pulled data from warmar pages.
"""


class Transaction:
    def __init__(self, order_type, platform, region, status, price):
        self.order_type = order_type
        self.platform = platform
        self.region = region
        self.status = status
        self.price = price


"""
returns the raw html from a URL as a string. will throw exception and return none if html error occurs
"""


def get_raw(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_html_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


"""
checks if an html response is good
"""


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


"""
for logging html errors if they occur- expand as necessary
"""


def log_html_error(e):
    print(e)


"""
gets raw html from the market URL and slices it down to the relevant transaction section.
returns -1 if there is a failure, and the transaction section otherwise
"""


def get_transaction_data(url):
    raw_html = get_raw(url)
    if raw_html:
        html = BeautifulSoup(raw_html, 'html.parser')
        text = ''.join(html.findAll(text=True))
        # the HTML section between "payload" and "include" contains the buy/sell orders
        text = re.search('"payload"(.*)"include"', text)
        if text:
            return text.group()
        else:
            return -1
    else:
        return -1


"""
given the transaction section of a warframe.market page, return a list of transaction objects representing relevant 
info from page buy/sell orders. returns the list if successful, or -1 in case of error
"""


def get_transactions(data):
    transactions = []
    # get locations in the string for relevant data values
    order_types = [m.end() for m in re.finditer('"order_type": ', data)]
    platforms = [m.end() for m in re.finditer('"platform": ', data)]
    regions = [m.end() for m in re.finditer('"region": ', data)][::2]
    statuses = [m.end() for m in re.finditer('"status": ', data)]
    platinum_vals = [m.end() for m in re.finditer('"platinum": ', data)]
    # check that list lengths are consistent- error out if not
    length = len(order_types)
    if all(len(x) == length for x in (platforms, regions, statuses, platinum_vals)):
        # convert indices to values, removing extra chars
        for i in range(length):
            for j in (order_types, platforms, regions, statuses, platinum_vals):
                j[i] = data[j[i]:].partition(",")[0]
                j[i] = j[i].replace('}', '')
                j[i] = j[i].replace(']', '')
                j[i] = j[i].replace('"', '')
        # create transaction objects and return them
        for i in range(length):
            transactions.append(Transaction(order_types[i], platforms[i], regions[i], statuses[i], platinum_vals[i]))
        return transactions
    else:
        return -1


"""
given all the transactions from a warframe.market page, return a list of all prices from ingame, online, pc, en sellers 
as a sorted list of ints. returns the list if successful, or -1 in case of error
"""


def get_prices(transactions):
    prices = []
    for i in transactions:
        if i.order_type == 'sell' and i.platform == 'pc' and i.region == 'en' and i.status == 'ingame':
            prices.append(int(i.price))
    prices.sort()
    return prices


"""
user facing function for war.mar calls aimed at price checking: given a valid warframe.market url, get sorted list of 
relevant transactions. will make attempts over and over until/unless successful; timeout behavior is TBD
"""


def query_market(url):
    data = -1
    transactions = -1
    # until good data is acquired, query war.mar
    while data == -1:
        data = get_transaction_data(url)
        # if the data was good, try to get prices from it
        if data != -1:
            transactions = get_transactions(data)
        # if prices couldn't be gotten, try again with new data
        if transactions == -1:
            data = -1
    return get_prices(transactions)


"""
generate a valid war.mar URL given a specific item. the market does not use the full item name for certain
items so this function accounts for that
"""


def generate_url(item):
    rooturl = 'https://warframe.market/items/'
    removed_words = ['Systems', 'Neuroptics', 'Chassis', 'Cerebrum', 'Carapace']
    # remove the word Blueprint if it contains a component blueprint name
    for word in removed_words:
        if word in item:
            item = item.replace(' Blueprint', "")

    # lower the string and replace spaces with underscores
    temp = item.lower()
    temp = temp.replace(' ', '_')

    return rooturl + temp


def multithread_query(url, result):
    result += query_market(url)


"""
get the price of the individual items of a relic 
"""


def get_relic_item_prices(input_relic, relics):
    result = [[] for i in range(6)]
    threads = []
    index = 0

    for relic in relics:
        if input_relic.lower() == relic.name.lower():

            for common in relic.commons:
                if common != 'Forma Blueprint':
                    thread_obj = threading.Thread(target=multithread_query, args=[generate_url(common), result[index]])
                    threads.append(thread_obj)
                    thread_obj.start()
                else:
                    result[index] = [35/3]
                index += 1
            for uncommon in relic.uncommons:
                if uncommon != 'Forma Blueprint':
                    thread_obj = threading.Thread(target=multithread_query, args=[generate_url(uncommon), result[index]])
                    threads.append(thread_obj)
                    thread_obj.start()
                else:
                    result[index] = [35/3]
                index += 1
            thread_obj = threading.Thread(target=multithread_query, args=[generate_url(relic.rare), result[index]])
            threads.append(thread_obj)
            thread_obj.start()
            index += 1

            for thread_obj in threads:
                thread_obj.join()

            return result

    return -1
