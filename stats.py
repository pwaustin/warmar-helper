import operator

"""
given a list of lists of prices, return a list of expected values for each. the take_average parameter determines 
whether the average price in the list is used or simply the lowest value
"""


def get_expected_prices(prices, take_average):
    expected_prices = []
    for price_set in prices:
        if take_average is True:
            expected_prices.append(sum(price_set)/float(len(price_set)))
        else:
            expected_prices.append(price_set[0])
    return expected_prices


"""
given a list of prices, return the expected value of the relic based on its quality. share argument supposes EV with 
4 identical relics used in a run if true
"""


def get_expected_value(prices, relic_quality, share):
    chance = {'intact': [.2533, .11, .02], 'exceptional': [.2333, .13, .04],
              'flawless': [.20, .17, .06],     'radiant': [.1667, .20, .1]}
    drop_type = {'common': 0, 'uncommon': 1, 'rare': 2}

    total_expected_value = 0
    pairs = []

    # map from array position to item quality
    for i in range(0, len(prices)):
        if i < 3:
            item_quality = drop_type['common']
        elif i < 5:
            item_quality = drop_type['uncommon']
        else:
            item_quality = drop_type['rare']

        # if not sharing, EV is the sum of prices times chance of item of that price appearing
        if not share:
            total_expected_value += prices[i] * chance[relic_quality][item_quality]
        # if sharing, store the price/chance pair as a tuple
        else:
            pairs.append((prices[i], chance[relic_quality][item_quality]))

    if not share:
        return total_expected_value

    else:
        pairs.sort(key=operator.itemgetter(0), reverse=True)
        average = 0
        seen = 0
        norm = 1
        for pair in pairs:
            price = pair[0]
            chance = pair[1]
            average += price * (1 - ((1-seen-chance)/(1-seen)) ** 4) * norm
            norm *= ((1-seen-chance)/(1-seen)) ** 4
            seen += chance

        return average
