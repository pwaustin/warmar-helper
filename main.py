import reliclib
import marketquery
import stats

relics = reliclib.generate_relics('relics.csv')
relic_price_list = marketquery.get_relic_item_prices('Neo R1', relics)

print(relic_price_list)
print(stats.get_expected_value(relic_price_list, 'intact', True, False))
print(stats.get_expected_value(relic_price_list, 'intact', False, False))
print(stats.get_expected_value(relic_price_list, 'radiant', True, False))
print(stats.get_expected_value(relic_price_list, 'radiant', False, False))
