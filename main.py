import reliclib
import marketquery
import stats

relics = reliclib.generate_relics('relics.csv')
relic_price_list = marketquery.get_relic_item_prices('Axi L1', relics)

print(relic_price_list)

prices = stats.get_expected_prices(relic_price_list, True)
print(stats.get_expected_value(prices, 'radiant', False))
print(stats.get_expected_value(prices, 'radiant', True))
