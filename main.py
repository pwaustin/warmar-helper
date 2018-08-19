import reliclib
import marketquery

relics = reliclib.generate_relics('relics.csv')


relic_price_list = marketquery.get_relic_item_prices('Neo R1', relics)

for item in testrelic:
    print(item)