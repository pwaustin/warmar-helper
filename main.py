import reliclib
import marketquery
import stats

relics = reliclib.generate_relics('relics.csv')

chosen_relic = input('Enter the name of your relic: ')
user_relic = reliclib.make_relic(chosen_relic, relics)

if user_relic:
    print('Relic has been found!\nProcessing...')
    relic_price_list = marketquery.get_relic_item_prices(chosen_relic, relics)
    print(relic_price_list)
    prices = stats.get_expected_prices(relic_price_list, True)
    print(stats.get_expected_value(prices, 'radiant', False))
    print(stats.get_expected_value(prices, 'radiant', True))
else:
    print('Error: Invalid relic name.')



