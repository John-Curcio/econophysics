import sys
import numpy as np
import csv
import matplotlib.pyplot as plt
import simStock as ss 

#TODO: twitter.csv only has the last three weeks' worth of closing prices
def getClosingPrices():
    closingPrices = []
    with open("HistoricalQuotes.csv", newline='') as csvfile:
        closingPriceReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in closingPriceReader:
            if row[1] != "close":
                closingPrices.append(float(row[4]))
    closingPrices.reverse()
    return closingPrices

def main():
    closingPrices = getClosingPrices()
    dailyReturnRates = [None]*(len(closingPrices) - 1)
    for i in range(1, len(closingPrices)):
        dailyReturnRates[i - 1] = (closingPrices[i] - closingPrices[i-1]) 
        dailyReturnRates[i - 1] /= 0.5*(closingPrices[i] + closingPrices[i-1])
    muHat = np.mean(dailyReturnRates)
    sigmaHat = np.std(dailyReturnRates, ddof=1)
    print("Twitter shares' daily return rate, volatility, and current price are all estimated from historical data. The risk-free interest rate is taken to be 1%, and S is the most recent closing price.")
    T = 100
    X = 14.0
    N = 1000
    n = 30
    default = input("\nWould you like to run the simulation with default parameters? [Y/N] : ")
    if default == "N" or default == "n":
        T = float(input("Days till this option's expiry date: "))
        X = float(input("This option's strike price: "))
        N = int(input("Time steps per simulation: "))
        n = int(input("Number of simulation paths: "))
    ss.simStock(r=0.01, mu=muHat, sigma=sigmaHat, T=T, S=closingPrices[-1], 
             X=X, N=N, n=n)

if __name__ == '__main__':
    main()







