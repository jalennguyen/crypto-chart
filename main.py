import matplotlib
import matplotlib.animation as animation
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib import style
from matplotlib import pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc

import tkinter as tk
from tkinter import ttk

import requests

import pandas as pd
import numpy as np

import talib


matplotlib.use('TkAgg')
style.use('ggplot')

f = plt.figure(facecolor='#121212')
plt.rcParams['grid.linewidth'] = 0.1
plt.rcParams['axes.titlepad'] = 25

coin_id = 'BTC-USD'
coin_name = 'Bitcoin'
exchange = 'Coinbase'
program_name = 'coinbase'
sample_size = '30min'
candle_width = 0.008
counter = 9000
paneCount = 1

top_indicator = 'none'
bot_indicator = 'none'
main_indicator = 'none'
emas = []
smas = []

chart_load = True

dark_color = '#183A54'
light_color = '#00A3E0'


def load_chart(run):
    global chart_load
    if run == 'start':
        chart_load = True
    elif run == 'stop':
        chart_load = False


def add_mainindicator(ind):
    global main_indicator
    global counter

    if sample_size == 'tick':
        popupmsg('Indicators in Tick Data not availible')

    if ind != 'none':
        if main_indicator == 'none':
            if ind == 'sma':
                ask_main = tk.Tk()
                ask_main.wm_title('Periods?')
                label = ttk.Label(ask_main, text='Choose how many periods for SMA')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(ask_main)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global main_indicator
                    global counter

                    main_indicator = []

                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    main_indicator.append(group)
                    counter = 9000
                    ask_main.destroy()

                b = ttk.Button(ask_main, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

            if ind == 'ema':
                ask_main = tk.Tk()
                ask_main.wm_title('Periods?')
                label = ttk.Label(ask_main, text='Choose how many periods for EMA')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(ask_main)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global main_indicator
                    global counter

                    main_indicator = []

                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    main_indicator.append(group)
                    counter = 9000
                    ask_main.destroy()

                b = ttk.Button(ask_main, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

        else:
            if ind == 'sma':
                ask_main = tk.Tk()
                ask_main.wm_title('Periods?')
                label = ttk.Label(ask_main, text='Choose how many periods for SMA')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(ask_main)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global main_indicator
                    global counter

                    periods = (e.get())
                    group = []
                    group.append('sma')
                    group.append(int(periods))
                    main_indicator.append(group)
                    counter = 9000
                    ask_main.destroy()

                b = ttk.Button(ask_main, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

            if ind == 'ema':
                ask_main = tk.Tk()
                ask_main.wm_title('Periods?')
                label = ttk.Label(ask_main, text='Choose how many periods for EMA')
                label.pack(side='top', fill='x', pady=10)
                e = ttk.Entry(ask_main)
                e.insert(0, 10)
                e.pack()
                e.focus_set()

                def callback():
                    global main_indicator
                    global counter

                    periods = (e.get())
                    group = []
                    group.append('ema')
                    group.append(int(periods))
                    main_indicator.append(group)
                    counter = 9000
                    ask_main.destroy()

                b = ttk.Button(ask_main, text='Submit', width=10, command=callback)
                b.pack()
                tk.mainloop()

    else:
        main_indicator = 'none'


def add_topindicator(ind):
    global top_indicator
    global counter

    if sample_size == 'tick':
        popupmsg('Indicators in Tick Data not availible')

    if ind == 'none':
        top_indicator = ind
        counter = 9000

    elif ind == 'rsi':
        ask_rsi = tk.Tk()
        ask_rsi.wm_title('Periods?')
        label = ttk.Label(ask_rsi, text='Choose duration for RSI calculation')
        label.pack(side='top', fill='x', pady=10)

        e = ttk.Entry(ask_rsi)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global top_indicator
            global counter

            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)

            top_indicator = group
            counter = 9000
            ask_rsi.destroy()

        b = ttk.Button(ask_rsi, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif ind == 'macd':
        top_indicator = 'macd'
        counter = 9000


def add_botindicator(ind):
    global bot_indicator
    global counter

    if sample_size == 'tick':
        popupmsg('Indicators in Tick Data not availible')

    if ind == 'none':
        bot_indicator = ind
        counter = 9000

    elif ind == 'rsi':
        ask_rsi = tk.Tk()
        ask_rsi.wm_title('Periods?')
        label = ttk.Label(ask_rsi, text='Choose duration for RSI calculation')
        label.pack(side='top', fill='x', pady=10)

        e = ttk.Entry(ask_rsi)
        e.insert(0, 14)
        e.pack()
        e.focus_set()

        def callback():
            global bot_indicator
            global counter

            periods = (e.get())
            group = []
            group.append('rsi')
            group.append(periods)

            bot_indicator = group
            counter = 9000
            ask_rsi.destroy()

        b = ttk.Button(ask_rsi, text='Submit', width=10, command=callback)
        b.pack()
        tk.mainloop()

    elif ind == 'macd':
        bot_indicator = 'macd'
        counter = 9000


def change_samplesize(size, width):
    global counter
    global sample_size
    global candle_width

    sample_size = size
    counter = 9000
    candle_width = width


def change_exchange(new, pname):
    global exchange
    global counter
    global program_name

    exchange = new
    program_name = pname
    counter = 9000


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title('!')

    label = ttk.Label(popup, text=msg)
    label.pack(side='top', fill='x', pady=10)

    button1 = ttk.Button(popup, text='Okay', command=popup.destroy)
    button1.pack()
    popup.mainloop()


def animate(i):
    global refresh_rate
    global counter
    global current_price

    def rsi_indicator(price_data, location):
        if location == 'top':
            rsi = talib.RSI(price_data, int(top_indicator[1]))

            a0.plot_date(OHLC['datetime'], rsi, light_color, label='RSI')
            a0.set_facecolor('#121212')
            plt.setp(a0.spines.values(), linewidth=0.1)

            # rsi strength band
            a0.axhspan(30, 70, color='purple', alpha=0.4)
            a0.axhline(30, linestyle='--', linewidth=1, color='#EEEEEE', alpha=0.7)
            a0.axhline(70, linestyle='--', linewidth=1, color='#EEEEEE', alpha=0.7)

            # set y-axis labels
            a0.set_ylabel("RSI " + str(top_indicator[1]), color='#BDBDBD', fontsize=10)
            a0.yaxis.set_label_position('right')
            a0.yaxis.tick_right()

        if location == 'bot':
            rsi = talib.RSI(price_data, int(bot_indicator[1]))

            a3.plot_date(OHLC['datetime'], rsi, light_color, label='RSI')
            a3.set_facecolor('#121212')
            plt.setp(a3.spines.values(), linewidth=0.1)

            # rsi strength band
            a3.axhspan(30, 70, color='purple', alpha=0.4)
            a3.axhline(30, linestyle='--', linewidth=1, color='#EEEEEE', alpha=0.7)
            a3.axhline(70, linestyle='--', linewidth=1, color='#EEEEEE', alpha=0.7)

            # set y-axis labels
            a3.set_ylabel("RSI "+str(bot_indicator[1]), color='#BDBDBD', fontsize=10)
            a3.yaxis.set_label_position('right')
            a3.yaxis.tick_right()

    def compute_macd(price_data, location):
        macd, signal, hist = talib.MACD(price_data, fastperiod=12, slowperiod=26, signalperiod=9)

        if location == 'top':
            a0.plot(OHLC['datetime'], macd, color=dark_color, lw=2)
            a0.plot(OHLC['datetime'], signal, color=light_color, lw=1)
            a0.fill_between(OHLC['datetime'], hist, 0, alpha=0.5, facecolor=dark_color, edgecolor=dark_color)

            a0.set_facecolor('#121212')
            plt.setp(a0.spines.values(), linewidth=0.1)

            # set y-axis labels
            a0.set_ylabel("MACD", color='#BDBDBD', fontsize=10)
            a0.yaxis.set_label_position('right')
            a0.yaxis.tick_right()

        if location == 'bot':
            a3.plot(OHLC['datetime'], macd, color=dark_color, lw=2)
            a3.plot(OHLC['datetime'], signal, color=light_color, lw=1)
            a3.fill_between(OHLC['datetime'], hist, 0, alpha=0.5, facecolor=dark_color, edgecolor=dark_color)

            a3.set_facecolor('#121212')
            plt.setp(a3.spines.values(), linewidth=0.1)

            # set y-axis labels
            a3.set_ylabel("MACD", color='#BDBDBD', fontsize=10)
            a3.yaxis.set_label_position('right')
            a3.yaxis.tick_right()

    if chart_load:
        if paneCount == 1:
            if sample_size == 'tick':
                try:
                    if exchange == 'Coinbase':
                        a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)
                        a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                        # request tick data from api
                        endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/trades'
                        data = requests.get(url=endpoint).json()
                        data.reverse()
                        data = pd.DataFrame(data)
                        data[['price', 'size']] = data[['price', 'size']].astype(float)
                        data['side'] = data['side'].astype('string')
                        data['time'] = data['time'].astype('datetime64[s]')

                        all_dates = data['time'].tolist()

                        buys = data[(data['side'] == 'buy')]
                        buy_dates = buys['time'].tolist()

                        sells = data[(data['side'] == 'sell')]
                        sell_dates = sells['time'].tolist()

                        volume = data['size']

                        a.clear()

                        a.plot_date(buy_dates, buys['price'], 'g', label='buys')
                        a.plot_date(sell_dates, sells['price'], 'r', label='sells')
                        a.set_facecolor('#181818')
                        a2.set_facecolor('#181818')

                        plt.setp(a.spines.values(), linewidth=0.1)
                        plt.setp(a2.spines.values(), linewidth=0.1)

                        a2.fill_between(all_dates, 0, volume, facecolor=dark_color)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
                        plt.setp(a.get_xticklabels(), visible=False)

                        # set y-axis labels
                        a.set_ylabel('Price', color='#BDBDBD', fontsize=10)
                        a2.set_ylabel('Volume', color='#BDBDBD', fontsize=10)
                        a.yaxis.set_label_position('right')
                        a2.yaxis.set_label_position('right')
                        a.yaxis.tick_right()
                        a2.yaxis.tick_right()

                        a.legend(loc='upper left')

                        last = len(data['price']) - 1
                        a.set_title(f'{coin_name} ({coin_id[:-4]})  /  U.S. Dollar  /  {sample_size} \n$' + format(data['price'][last], ',.2f'), loc='left', fontsize=18, color='#BDBDBD')

                except Exception as e:
                    print('Failed because of ', e)

            else:
                if counter > 12:
                    try:
                        if exchange == 'Coinbase':
                            # using both indicators
                            if top_indicator != 'none' and bot_indicator != 'none':
                                # main graph
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=3, colspan=4)

                                #volume
                                a2 = plt.subplot2grid((6, 4), (4, 0), rowspan=1, colspan=4, sharex=a)

                                # bot indicator
                                a3 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                                # top indicator
                                a0 = plt.subplot2grid((6, 4), (0, 0), rowspan=1, colspan=4, sharex=a)

                            elif top_indicator != 'none':
                                # main graph
                                a = plt.subplot2grid((6, 4), (1, 0), rowspan=4, colspan=4)

                                # volume
                                a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                                # top indicator
                                a0 = plt.subplot2grid((6, 4), (0, 0), rowspan=1, colspan=4, sharex=a)

                            elif bot_indicator != 'none':
                                # main graph
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=4, colspan=4)

                                # volume
                                a2 = plt.subplot2grid((6, 4), (4, 0), rowspan=1, colspan=4, sharex=a)

                                # bot indicator
                                a3 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                            else:
                                # main graph
                                a = plt.subplot2grid((6, 4), (0, 0), rowspan=5, colspan=4)

                                # volume
                                a2 = plt.subplot2grid((6, 4), (5, 0), rowspan=1, colspan=4, sharex=a)

                        # timeframe = data_pace
                        if sample_size in ('1min', '3min'):
                            endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/candles?granularity=60'

                        elif sample_size == '5min':
                            endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/candles?granularity=300'

                        elif sample_size in ('15min', '30min', '45min'):
                            endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/candles?granularity=900'

                        elif sample_size in ('1h', '2h', '3h', '4h'):
                            endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/candles?granularity=3600'

                        elif sample_size in ('1d', '1w', '1m'):
                            endpoint = f'https://api.pro.coinbase.com/products/{coin_id}/candles?granularity=86400'

                        # request historical data from api
                        data = requests.get(url=endpoint).json()
                        data.reverse()

                        keys = ['datetime', 'low', 'high', 'open', 'close', 'volume']
                        OHLC = [dict(zip(keys, x)) for x in data]
                        OHLC = pd.DataFrame(OHLC)

                        OHLC['datetime'] = OHLC['datetime'].astype('datetime64[s]')
                        OHLC = OHLC.set_index('datetime')

                        # resample ohlc data
                        ohlc = {
                            'open': 'first',
                            'high': 'max',
                            'low': 'min',
                            'close': 'last',
                            'volume': 'sum'
                        }
                        OHLC = OHLC.resample(sample_size).apply(ohlc)

                        OHLC.reset_index(inplace=True)
                        OHLC['datetime'] = mdates.date2num(OHLC['datetime'])

                        a.clear()
                        a.set_facecolor('#181818')
                        a2.set_facecolor('#181818')

                        if main_indicator != 'none':

                            for ma in main_indicator:
                                if ma[0] == 'sma':
                                    sma = OHLC['close'].rolling(ma[1]).mean()
                                    label = str(ma[1]) + ' SMA'
                                    a.plot(OHLC['datetime'], sma, label=label)

                                if ma[0] == 'ema':
                                    ewma = OHLC['close'].ewm(ma[1]).mean()
                                    label = str(ma[1]) + ' EMA'
                                    a.plot(OHLC['datetime'], ewma, label=label)

                            a.legend(loc=0)

                        price_data = np.array(OHLC['close'])
                        last = len(OHLC['close']) - 1
                        # Top indicator
                        if top_indicator[0] == 'rsi':
                            rsi_indicator(price_data, 'top')
                            a0.set_title(f'{coin_name} ({coin_id[:-4]})  /  U.S. Dollar  /  {sample_size} \n$'
                                         + format(OHLC['close'][last], ',.2f'),
                                         loc='left', fontsize=18, color='#BDBDBD')

                        elif top_indicator == 'macd':
                            compute_macd(price_data, 'top')
                            a0.set_title(f'{coin_name} ({coin_id[:-4]})  /  U.S. Dollar  /  {sample_size} \n$'
                                         + format(OHLC['close'][last], ',.2f'),
                                         loc='left', fontsize=18, color='#BDBDBD')

                        else:  # no top chart
                            a.set_title(f'{coin_name} ({coin_id[:-4]})  /  U.S. Dollar  /  {sample_size} \n$'
                                        + format(OHLC['close'][last], ',.2f'),
                                        loc='left', fontsize=18, color='#BDBDBD')

                        # Bottom Indicator
                        if bot_indicator[0] == 'rsi':
                            rsi_indicator(price_data, 'bot')

                        elif bot_indicator == 'macd':
                            compute_macd(price_data, 'bot')

                        candlestick_ohlc(a, OHLC[['datetime', 'open', 'high', 'low', 'close']].values,
                                         width=candle_width, colorup='g', colordown='r')

                        a2.fill_between(OHLC['datetime'], 0, OHLC['volume'], facecolor=dark_color)

                        a.xaxis.set_major_locator(mticker.MaxNLocator(3))
                        a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

                        a.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))

                        plt.setp(a.get_xticklabels(), visible=False)

                        plt.setp(a.spines.values(), linewidth=0.1)
                        plt.setp(a2.spines.values(), linewidth=0.1)

                        # set y-axis labels
                        a.set_ylabel('Price', color='#BDBDBD', fontsize=10)
                        a2.set_ylabel('Volume', color='#BDBDBD', fontsize=10)
                        a.yaxis.set_label_position('right')
                        a2.yaxis.set_label_position('right')
                        a.yaxis.tick_right()
                        a2.yaxis.tick_right()

                        if top_indicator != 'none':
                            plt.setp(a0.get_xticklabels(), visible=False)

                        if bot_indicator != 'none':
                            plt.setp(a2.get_xticklabels(), visible=False)

                        counter = 0

                    except Exception as e:
                        print('Failed in the non-tick animate: ', str(e))
                        counter = 9000

                else:
                    counter += 1

            f.align_labels()
            plt.subplots_adjust(left=.02, bottom=.11, right=.87, top=.8, wspace=.50, hspace=0.32)


class CryptoApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, 'CRYPTO')

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(container)

        # file menu
        filemenu = tk.Menu(menu_bar, tearoff=0)
        filemenu.add_command(label='Export chart', command=lambda: popupmsg('Feature coming soon!'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=quit)
        menu_bar.add_cascade(label='File', menu=filemenu)

        # select exchange
        exchange_choice = tk.Menu(menu_bar, tearoff=0)
        exchange_choice.add_command(label='Coinbase',
                                    command=lambda: change_exchange('Coinbase', 'coinbase'))
        exchange_choice.add_command(label='Binance',
                                    command=lambda: popupmsg('Feature coming soon!'))
        exchange_choice.add_command(label='Kraken',
                                    command=lambda: popupmsg('Feature coming soon!'))
        menu_bar.add_cascade(label='Exchange', menu=exchange_choice)

        # select OHLC interval
        ohlci = tk.Menu(menu_bar, tearoff=0)
        ohlci.add_command(label='Tick',
                          command=lambda: change_samplesize('tick', 0))
        ohlci.add_separator()
        # minutes
        ohlci.add_command(label='1 Minute',
                          command=lambda: change_samplesize('1min', 0.0005))
        ohlci.add_command(label='5 Minute',
                          command=lambda: change_samplesize('5min', 0.003))
        ohlci.add_command(label='15 Minute',
                          command=lambda: change_samplesize('15min', 0.008))
        ohlci.add_command(label='30 Minute',
                          command=lambda: change_samplesize('30min', 0.016))
        ohlci.add_separator()
        # hours
        ohlci.add_command(label='1 hour',
                          command=lambda: change_samplesize('1h', 0.032))
        ohlci.add_command(label='2 hours',
                          command=lambda: change_samplesize('2h', 0.096))
        ohlci.add_command(label='3 hours',
                          command=lambda: change_samplesize('3h', 0.096))
        ohlci.add_command(label='4 hours',
                          command=lambda: change_samplesize('4h', 0.096))
        ohlci.add_separator()
        #  days+
        ohlci.add_command(label='1 day',
                          command=lambda: change_samplesize('1d', 0.032))
        ohlci.add_command(label='1 week',
                          command=lambda: change_samplesize('1w', 0.096))
        ohlci.add_command(label='1 month',
                          command=lambda: change_samplesize('1m', 0.096))
        menu_bar.add_cascade(label='OHLC Interval', menu=ohlci)

        # select main indicator
        main_indi = tk.Menu(menu_bar, tearoff=0)
        main_indi.add_command(label='SMA',
                              command=lambda: add_mainindicator('sma'))
        main_indi.add_command(label='EMA',
                              command=lambda: add_mainindicator('ema'))
        main_indi.add_separator()
        main_indi.add_command(label='None',
                              command=lambda: add_mainindicator('none'))
        menu_bar.add_cascade(label='Main Indicator', menu=main_indi)

        # select top indicator
        top_indi = tk.Menu(menu_bar, tearoff=0)
        top_indi.add_command(label='RSI',
                             command=lambda: add_topindicator('rsi'))
        top_indi.add_command(label='MACD',
                             command=lambda: add_topindicator('macd'))
        top_indi.add_separator()
        top_indi.add_command(label='None',
                             command=lambda: add_topindicator('none'))

        menu_bar.add_cascade(label='Top Indicator', menu=top_indi)

        # select bottom indicator
        bot_indi = tk.Menu(menu_bar, tearoff=0)
        bot_indi.add_command(label='RSI',
                             command=lambda: add_botindicator('rsi'))
        bot_indi.add_command(label='MACD',
                             command=lambda: add_botindicator('macd'))
        bot_indi.add_separator()
        bot_indi.add_command(label='None',
                             command=lambda: add_botindicator('none'))
        menu_bar.add_cascade(label='Bottom Indicator', menu=bot_indi)

        # freezing chart
        start_stop = tk.Menu(menu_bar, tearoff=0)
        start_stop.add_command(label='Pause',
                               command=lambda: load_chart('stop'))
        start_stop.add_separator()
        start_stop.add_command(label='Resume',
                               command=lambda: load_chart('start'))
        menu_bar.add_cascade(label='Freeze Client', menu=start_stop)

        tk.Tk.config(self, menu=menu_bar)

        self.frames = {}
        frame = GraphPage(container, self)
        self.frames[GraphPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(GraphPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GraphPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.configure(self, bg='#121212')

        # set up grid
        tk.Frame.grid_rowconfigure(self, 0, weight=15)
        tk.Frame.grid_rowconfigure(self, 1, weight=1)

        tk.Frame.columnconfigure(self, 0, weight=1)
        tk.Frame.columnconfigure(self, 1, weight=10)
        tk.Frame.columnconfigure(self, 2, weight=10)
        tk.Frame.columnconfigure(self, 3, weight=2)
        tk.Frame.columnconfigure(self, 4, weight=1)

        # set matplotlib canvas
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, columnspan=4, sticky='nsew')

        # place matplotlib graph toolbar
        tool_frame = tk.Frame(self)
        tool_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        NavigationToolbar2Tk(canvas, tool_frame)

        # insert search entry
        search_box = ttk.Entry(self, width=12)
        search_box.grid(row=1, column=3, sticky='nsew')

        def search_coin():
            global coin_id
            global coin_name
            global counter

            endpoint = 'https://api.pro.coinbase.com/currencies'
            coins = requests.get(url=endpoint).json()

            search = search_box.get()

            for coin in coins:
                # if searched coin exists, update current coin
                if coin['id'].lower() == search.lower() or coin['name'].lower() == search.lower():
                    coin_id = coin['id']+"-USD"
                    coin_name = coin['name']
                    counter = 9000
                    return

            popupmsg(f'Cryptocurrency "{search}" not found!')

        search_btn = ttk.Button(self, text='Search', command=search_coin)
        search_btn.grid(row=1, column=4, sticky='nsew')


app = CryptoApp()
app.geometry('1280x720')
ani = animation.FuncAnimation(f, animate, interval=2000)
app.mainloop()
