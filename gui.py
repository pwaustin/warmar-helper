from tkinter import ttk
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font
import reliclib
import marketquery
import stats




class AutoGrid(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.columns = None
        self.bind('<Configure>', self.regrid)

    def regrid(self, event=None):
        width = self.winfo_width()
        slaves = self.grid_slaves()
        max_width = max(slave.winfo_width() for slave in slaves)
        cols = width // max_width
        if cols == self.columns: # if the column number has not changed, abort
            return
        for i, slave in enumerate(reversed(slaves)):
            slave.grid_forget()
            slave.grid(row=i//cols, column=i%cols)
        self.columns = cols

class RelicButton(tk.Frame):
    def __init__(self, relic, relics, text, master=None, **kwargs):
        tk.Frame.__init__(self, master, bd=5, relief=tk.RAISED, **kwargs)

        helv36 = font.Font(family='Helvetica', size=20, weight='bold')

        tk.Label(self, font=helv36, text=relic.name.split()[1]).grid(row=0, column=1, columnspan=4)
        tk.Button(self, text='I', width=2, command = lambda relic=relic: calc_relic(relic, relics, 'intact', text)).grid(row=1, column=1)
        tk.Button(self, text='F', width=2, command = lambda relic=relic: calc_relic(relic, relics, 'flawless', text)).grid(row=1, column=2)
        tk.Button(self, text='E', width=2, command = lambda relic=relic: calc_relic(relic, relics, 'exceptional', text)).grid(row=1, column=3)
        tk.Button(self, text='R', width=2, command = lambda relic=relic: calc_relic(relic, relics, 'radiant', text)).grid(row=1, column=4)


def append_text(message, text):
    text.configure(state='normal')
    text.insert(tk.END, message + '\n')
    text.configure(state='disabled')
    # Autoscroll to the bottom
    text.yview(tk.END)

def calc_relic(relic, relics, quality, text):
            trust_lowest = False

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
            prices = stats.get_expected_prices(relic_price_list, trust_lowest)
            append_text('Expected value for single use: ' + str(stats.get_expected_value(prices, quality, False)), text)
            append_text('Expected value for relic share: ' + str(stats.get_expected_value(prices, quality, True)), text)
            append_text('', text)


def gui():
    root = tk.Tk()
    root.title("WarMar Helper")

    nb = ttk.Notebook(root)
    nb.pack(expand=True, fill="both")

    # adding Frames as pages for the ttk.Notebook 
    # first page, which would get widgets gridded into it
    lith = AutoGrid(nb)
    meso = AutoGrid(nb)
    neo = AutoGrid(nb)
    axi = AutoGrid(nb)

    lith.pack(expand=True, fill="both")
    meso.pack(expand=True, fill="both")
    neo.pack(expand=True, fill="both")
    axi.pack(expand=True, fill="both")

    relics = reliclib.generate_relics('relics.csv')

    helv36 = font.Font(family='Helvetica', size=20, weight='bold')

    # second page
    page2 = ttk.Frame(root)
    text = ScrolledText(page2)
    text.pack(expand=1, fill="both")

    for relic in relics:
        if relic.name.startswith('Lith'):
            #b = tk.Button(lith, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text))
            #tk.Button(lith, text=relic.name.split()[1], font=helv36, command = lambda relic=relic: calc_relic(relic, relics, text)).grid()
            RelicButton(relic=relic, relics=relics, text=text, master=lith).grid()
        elif relic.name.startswith('Meso'):
            RelicButton(relic=relic, relics=relics, text=text, master=meso).grid()
        elif relic.name.startswith('Neo'):
            RelicButton(relic=relic, relics=relics, text=text, master=neo).grid()
        elif relic.name.startswith('Axi'):
            RelicButton(relic=relic, relics=relics, text=text, master=axi).grid()

    

    nb.add(lith, text='Lith')
    nb.add(meso, text='Meso')
    nb.add(neo, text='Neo')
    nb.add(axi, text='Axi')

    
    page2.pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    gui()