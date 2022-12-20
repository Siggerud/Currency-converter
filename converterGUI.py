from tkinter import Label, Tk, ttk, Entry, StringVar
from webscraper import getCurrencyCodesAndInfo, find_exchange_amount
from threading import Thread

# renskriv og legg i github

class converterGUI:
    def __init__(self, master):
        """This class builds a GUI for a currency converter"""
        self.master = master
        master.title("Currency converter")
        master.geometry("600x150")

        font_tuple = ("Arial", 10, "bold")

        amountLabel = Label(master, text="Amount", font=font_tuple)
        amountLabel.grid(row=0, column=0)

        self.amount = StringVar()
        self.amount.set(1)
        self.amount.trace("w", self.convert)
        amountEntry = Entry(master, textvariable=self.amount)
        amountEntry.grid(row=1, column=0, padx=10)

        convertFromLabel = Label(master, text="Convert from", font=font_tuple)
        convertFromLabel.grid(row=0, column=1)

        ConvertToLabel = Label(master, text="Convert to", font=font_tuple)
        ConvertToLabel.grid(row=0, column=2)

        self.countries = []
        self.currencies = []
        self.codes = []

        self.thread_trimming_process()

        values = []
        for country, code in zip(self.countries, self.codes):
            values.append(f"{country} - {code}")

        self.fromCurrency = StringVar()
        self.comboFrom = ttk.Combobox(master, values = values, textvariable=self.fromCurrency)
        self.comboFrom.bind("<<ComboboxSelected>>", self.convert)
        self.comboFrom.current(0)
        self.comboFrom.grid(row=1, column=1, ipadx=25, padx=10, pady=5)

        self.toCurrency = StringVar()
        self.comboTo = ttk.Combobox(master, values=values, textvariable=self.toCurrency)
        self.comboTo.bind("<<ComboboxSelected>>", self.convert)
        self.comboTo.current(20)
        self.comboTo.grid(row=1, column=2, ipadx=25)

        self.convertedAmount = StringVar()
        convertedLabel = Label(master, textvariable=self.convertedAmount, fg="blue")
        convertedLabel.grid(row=2, column=0, columnspan=3, sticky="w")

        self.convert()

    def thread_trimming_process(self):
        """Starts a multithreaded process to speed up 'trim_currency_options'"""
        countries, currencies, codes = getCurrencyCodesAndInfo()

        trimmingThreads = []
        for i in range(0, len(countries), 2):
            start = i
            end = i + 1
            trimmingThread = Thread(target=self.trim_currency_options, args=(countries, currencies, codes, start, end))
            trimmingThreads.append(trimmingThread)
            trimmingThread.start()

        for thread in trimmingThreads:
            thread.join()

    def trim_currency_options(self, countries, currencies, codes, start, end):
        """Trims the list of currencies used in the combobox based on if they show an exchange rate with USD"""
        fromCode = "USD"
        count= 0
        for index in range(start, end):
            toCode = codes[index]
            count += 1
            if find_exchange_amount(fromCode, toCode, 1) != "0.000000 ---":
                self.countries.append(countries[index])
                self.currencies.append(currencies[index])
                self.codes.append(codes[index])


    def convert(self, *args):
        """Gets and sets converted amount in GUI"""
        indexFrom = self.comboFrom.current()
        indexTo = self.comboTo.current()

        fromCode = self.codes[indexFrom]
        toCode = self.codes[indexTo]
        amount = self.amount.get()

        convertedAmount = find_exchange_amount(fromCode, toCode, amount)
        if convertedAmount == "0.000000 ---":
            convertedAmountText = f"No info on exchange rate between {self.currencies[indexFrom]} and {self.currencies[indexTo]}"
        else:
            convertedAmount = float(convertedAmount.split()[0])
            convertedAmountText = f"{amount} {self.currencies[indexFrom]}(s) is {convertedAmount:.3f} {self.currencies[indexTo]}(s)"

        self.convertedAmount.set(convertedAmountText)


master = Tk()
myGUI = converterGUI(master)
master.mainloop()
