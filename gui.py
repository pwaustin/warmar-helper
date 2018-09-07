from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
import reliclib
import marketquery
import stats


def append_text(message, text):
    text.configure(state='normal')
    text.insert(tk.END, message + '\n')
    text.configure(state='disabled')
    # Autoscroll to the bottom
    text.yview(tk.END)

def calc_relic(relic, relics, text):
            quality = 'radiant'
            use_average = False

            append_text(relic.name, text)
            relic_price_list = marketquery.get_relic_item_prices(relic.name, relics)
            append_text('Relic contains:', text)
            for i in range(0, 6):
                if i < 3:
                    append_text('Common: ' + relic.commons[i], text)
                elif i < 5:
                    append_text('Uncommon: ' + relic.uncommons[i-3], text)
                else:
                    append_text('Rare: ' + relic.rare, text)
                append_text(str(relic_price_list[i]), text)
            prices = stats.get_expected_prices(relic_price_list, use_average)
            append_text('Expected value for single use: ' + str(stats.get_expected_value(prices, quality, False)), text)
            append_text('Expected value for relic share: ' + str(stats.get_expected_value(prices, quality, True)), text)
            append_text('', text)


def gui():
    root = tk.Tk()
    root.title("ttk.Notebook")

    nb = ttk.Notebook(root)

    # adding Frames as pages for the ttk.Notebook 
    # first page, which would get widgets gridded into it
    lith = ttk.Frame(nb)
    meso = ttk.Frame(nb)
    neo = ttk.Frame(nb)
    axi = ttk.Frame(nb)

    relics = reliclib.generate_relics('relics.csv')

    helv36 = font.Font(family='Helvetica', size=20, weight='bold')

    # second page
    page2 = ttk.Frame(root)
    text = ScrolledText(page2)
    text.pack(expand=1, fill="both")

    for relic in relics:
        if relic.name.startswith('Lith'):
            b = tk.Button(lith, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text))
            b.pack(side = tk.LEFT)
        elif relic.name.startswith('Meso'):
            b = tk.Button(meso, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text))
            b.pack(side = tk.LEFT)
        elif relic.name.startswith('Neo'):
            b = tk.Button(neo, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text))
            b.pack(side = tk.LEFT)
        elif relic.name.startswith('Axi'):
            b = tk.Button(axi, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text))
            b.pack(side = tk.LEFT)

    

    nb.add(lith, text='Lith')
    nb.add(meso, text='Meso')
    nb.add(neo, text='Neo')
    nb.add(axi, text='Axi')

    nb.pack(expand=1, fill="both")
    page2.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    gui()