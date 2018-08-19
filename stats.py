"""
given a list of prices, return the expected value of the relic based on its quality. average argument controls whether
average price or lowest price is used in the calculation. radshare argument supposes EV with 4 identical relics used in
a run
"""


def get_expected_value(prices, relic_quality, take_average, rad_share):
    chance = {'intact': [.2533, .11, .02], 'exceptional': [.2333, .13, .04],
              'flawless': [.20, .17, .06], 'radiant': [.1667, .20, .1]}
    drop_type = {'common': 0, 'uncommon': 1, 'rare': 2}
    total_expected_value = 0
    if not rad_share:
        for i in range(0, len(prices)):
            if i < 3:
                item_quality = drop_type['common']
            elif i < 5:
                item_quality = drop_type['uncommon']
            else:
                item_quality = drop_type['rare']

            if not take_average:
                total_expected_value += prices[i][0] * chance[relic_quality][item_quality]
            else:
                total_expected_value += (sum(prices[i])/float(len(prices[i]))) * chance[relic_quality][item_quality]
    else:
        total_expected_value = -1  # temp value
    return total_expected_value


