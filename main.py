import reliclib
import marketquery
import stats

use_average = False
relics = reliclib.generate_relics('relics.csv')

while True:
    chosen_relic = input('Enter the name of your relic, or select \'exit\': ')
    user_relic = reliclib.make_relic(chosen_relic, relics)
    if chosen_relic == 'exit':
        break
    elif user_relic:
        quality = input('Enter relic quality: ')
        if quality == 'intact' or quality == 'radiant' or quality == 'exceptional' or quality == 'flawless':
            print('Relic has been found!\nProcessing...')
            relic_price_list = marketquery.get_relic_item_prices(chosen_relic, relics)
            print('Relic contains:')
            for i in range(0, 6):
                if i < 3:
                    print('Common: ' + user_relic.commons[i])
                elif i < 5:
                    print('Uncommon: ' + user_relic.uncommons[i-3])
                else:
                    print('Rare: ' + user_relic.rare)
                print(relic_price_list[i])
            prices = stats.get_expected_prices(relic_price_list, use_average)
            print('Expected value for single use: ' + str(stats.get_expected_value(prices, quality, False)))
            print('Expected value for relic share: ' + str(stats.get_expected_value(prices, quality, True)))
        else:
            print('Error: Invalid relic quality. Please try again.')
    else:
        print('Error: Invalid relic name. Please try again.')
