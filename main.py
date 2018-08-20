import reliclib
import marketquery
import stats

relics = reliclib.generate_relics('relics.csv')

while True:
    chosen_relic = input('Enter the name of your relic: ')
    user_relic = reliclib.make_relic(chosen_relic, relics)
    if chosen_relic == 'exit':
        break
    elif user_relic:
        quality = input('Enter relic quality: ')
        if quality == 'intact' or quality == 'radiant' or quality == 'exceptional' or quality == 'flawless':
            print('Relic has been found!\nProcessing...')
            relic_price_list = marketquery.get_relic_item_prices(chosen_relic, relics)
            for i in range (0, 6):
                if i < 3:
                    print(user_relic.commons[i])
                elif i < 5:
                    print(user_relic.uncommons[i-3])
                else:
                    print(user_relic.rare)
                print(relic_price_list[i])
            prices = stats.get_expected_prices(relic_price_list, True)
            print('Expected value for single use: ' + str(stats.get_expected_value(prices, quality, False)))
            print('Expected value for relic share: ' + str(stats.get_expected_value(prices, quality, True)))
        else:
            print('Error: Invalid relic quality. Please try again.')
    else:
        print('Error: Invalid relic name.')



