##
#
# @author Ricardo Trevisan
# 2020, December
# Analytic trading experiences
#
# Generosity, Morality, Concentration, Patience, Enthusiastic Effort and Wisdom
# The Six Perfections 
#
##

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go


def plot_data(df, title, xlabel, ylabel):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left')
    plt.show()

def run():
    symbol = 'PETR4.SA'
    dtStart = '2020-12-01'
    dtEnd = '2020-12-04'
    
    #df = yf.Ticker(symbol).history(start=dtStart, end=dtEnd, interval='1m')
    df = yf.Ticker(symbol).history(start=dtStart, end=dtEnd, interval='1d')

    last_day = df.tail(1).copy()
    last_day['Pivot'] = (last_day['High'] + last_day['Low'] + last_day['Close'])/3
    last_day['R1'] = 2*last_day['Pivot'] - last_day['Low']
    last_day['S1'] = 2*last_day['Pivot'] - last_day['High']
    last_day['R2'] = last_day['Pivot'] + (last_day['High'] - last_day['Low'])
    last_day['S2'] = last_day['Pivot'] - (last_day['High'] - last_day['Low'])
    last_day['R3'] = last_day['Pivot'] + 2*(last_day['High'] - last_day['Low'])
    last_day['S3'] = last_day['Pivot'] - 2*(last_day['High'] - last_day['Low'])

    pivotado = (df.High + df.Low + df.Close)/3

    candles = {
    'x': df.index,
    'open': df.Open,
    'close': df.Close,
    'high': df.High,
    'low': df.Low,
    'type': 'candlestick',
    'name': symbol,
    'showlegend': True
    }
    
    avg30 = df.Close.rolling(window=30, min_periods=1).mean()
    avrg = {
    'x': df.index,
    'y': avg30,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'blue'
            },
    'name': 'Moving Average of 30 periods'
    }

    pivot = {
    'x': df.index,
    'y': pivotado,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 3,
        'color': 'purple'
            },
    'name': 'Pivot Info'
    }
 
    data = [candles, pivot, avrg]
    layout = go.Layout({
        'title': {
            'text': 'Trading Analysis',
            'font': {
                'size': 15
            }
        }
    })

    fig = go.Figure(data=data, layout=layout)
    fig.show()

if __name__ == "__main__":
    run()
