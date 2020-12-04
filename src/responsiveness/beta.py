##
#
# @author Ricardo Trevisan
# 2020, December
# Analytic trading experiences
#
#
##

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from statsmodels import regression


def plot_data(df, title, xlabel, ylabel):
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left')
    plt.show()

def get_data(symbols, dtInicio, dtFim):
    dates = pd.date_range(dtInicio, dtFim)
    df = pd.DataFrame(index=dates)

    for symbol in symbols:

        df_temp = yf.Ticker(symbol).history(start=dtInicio, end=dtFim)
        df_temp = df_temp.rename(columns={"Close": symbol})

        # Abstract columns
        df_temp = df_temp[symbol]

        df = df.join(df_temp)
        if symbol == '%5EBVSP':
            df = df.dropna(subset=['%5EBVSP'])  # exclude NaN lines based on BOVA11

        if symbol == "SPY":
            df = df.dropna(subset=["SPY"])       # exclude NaN lines based on BOVA11
        df.fillna(method="ffill", inplace=True)  #filling gaps forwardly
        df.fillna(method="bfill", inplace=True)  # filling gaps backly
    return df

def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = ((df[1:] / df[:-1].values) - 1)*100
    daily_returns.iloc[0, :] = 0 #set daily returns for row 0
    return daily_returns

def linreg(x, y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y, x).fit()

    # We are removing the constant
    x = x[:, 1]
    return model.params[0], model.params[1]

def run():

    dtinicio = '2019-01-01'
    dt_fim = '2020-12-31'
    
    #Bench vs Option
    symbols = ['%5EBVSP', 'PETR4.SA']
    #symbols = ['%5EBVSP', 'LUPA3.SA']

    df = get_data(symbols, dtinicio, dt_fim)
    daily_returns = compute_daily_returns(df)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    
    #Calculating Alpha & Beta
    X = daily_returns[symbols[0]].values
    Y = daily_returns[symbols[1]].values

    #OLS
    alpha, beta = linreg(X,Y)
    print(symbols[1], 'alpha: ' + str(alpha))
    print(symbols[1], 'beta: ' + str(beta))

    X2 = np.linspace(X.min(), X.max(), 100)
    Y_hat = X2 * beta + alpha

    plt.figure(figsize=(10,7))
    plt.scatter(X, Y, alpha=0.3) # Plot the raw data
    plt.xlabel(symbols[0] + " Daily Return")
    plt.ylabel(symbols[1] + " Daily Return")

    plt.plot(X2, Y_hat, 'r', alpha=0.9)
    plt.show()

    print("Scatterplots Branch: Going forward...")
    print("New Branch Scatterplots")


if __name__ == "__main__":
    run()
