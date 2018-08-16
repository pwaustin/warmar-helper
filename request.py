from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re

"""
returns the raw html from a URL as a string. 
will throw exception and return none if html error occurs
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
def getTransactionData(url):
  raw_html = get_raw(url)
  if raw_html:
    html = BeautifulSoup(raw_html, 'html.parser')
    text = ''.join(html.findAll(text=True))
    #the HTML section between "payload" and "include" contains the buy/sell orders
    text = re.search('"payload"(.*)"include"', text)
    if text:
      return text.group()
    else:
      return -1
  else:
    return -1

"""
given the transaction section of a warframe.market page, return a list of all prices
from ingame, online, pc, en sellers as a sorted list of ints.
returns the list if successful, or -1 in case of error
"""
def getPrices(data):
  prices = []
  #get locations in the string for relevant data values
  orderTypes = [m.end() for m in re.finditer('"order_type": ', data)]
  platforms = [m.end() for m in re.finditer('"platform": ', data)]
  regions = [m.end() for m in re.finditer('"region": ', data)][::2]
  statuses = [m.end() for m in re.finditer('"status": ', data)]
  platinumVals = [m.end() for m in re.finditer('"platinum": ', data)]
  #check that list lengths are consistent- error out if not
  length = len(orderTypes)
  if all(len(x) == length for x in (platforms,regions,statuses,platinumVals)):
    #convert indices to values, removing extra chars
    for i in range(length):
      for j in (orderTypes,platforms,regions,statuses,platinumVals):
        j[i] = data[j[i]:].partition(",")[0]
        j[i] = j[i].replace('}','')
        j[i] = j[i].replace('"','')
    #save int plat values from sell orders on pc/en where the user is ingame
    for i in range(length):
      if orderTypes[i] == 'sell' and platforms[i] == 'pc' and regions[i] == 'en' and statuses[i] == 'ingame':
        prices.append(int(platinumVals[i]))
    prices.sort()
    return prices
  else:
    return -1

"""
user facing function for war.mar calls aimed at price checking: 
given a valid warframe.market url, get sorted list of relevant prices.
will make attempts over and over until/unless successful;
timeout behavior is TBD
"""
def queryMarket(url):
  data = -1
  prices = -1
  #until good data is acquired, query war.mar
  while data == -1:
    data = getTransactionData(url)
    #if the data was good, try to get prices from it
    if data != -1:
      prices = getPrices(data)
    #if prices couldn't be gotten, try again with new data
    if prices == -1:
      data = -1
  return prices

#test a valid war.mar URL here
print(queryMarket('https://warframe.market/items/akbolto_prime_receiver'))