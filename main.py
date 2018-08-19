import reliclib
import marketquery

relics = reliclib.generate_relics('relics.csv')
marketquery.get_relic_item_prices('Neo R1', relics)