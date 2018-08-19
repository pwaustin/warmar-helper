"""
given a list of prices, return the expected value of the relic based on its quality. average argument controls whether
average price or lowest price is used in the calculation
"""


def get_expected_value(prices, relic_quality, take_average, rad_share):
    chance = {'intact': [.2533, .11, .02], 'exceptional': [.2333, .13, .04],
              'flawless': [.20, .34, .06], 'radiant': [.5, .40, .1]}
    drop_type = {'bronze': 0, 'silver': 1, 'gold': 2}
    total_expected_value = 0
    if not rad_share:
        for i in range(0, len(prices)):
            if i < 3:
                item_quality = drop_type['bronze']
            elif i < 5:
                item_quality = drop_type['silver']
            else:
                item_quality = drop_type['gold']

            if not take_average:
                total_expected_value += prices[i][0] * chance[relic_quality][item_quality]
            else:
                total_expected_value += (sum(prices[i])/float(len(prices[i]))) * chance[relic_quality][item_quality]
    else:
        total_expected_value = -1  # temp value
    return total_expected_value


