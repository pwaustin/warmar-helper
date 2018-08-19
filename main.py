import reliclib
import marketquery
import stats

relics = reliclib.generate_relics('relics.csv')
relic_price_list = marketquery.get_relic_item_prices('Neo R1', relics)
