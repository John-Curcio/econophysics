import sys
import numpy as np
import csv
import matplotlib.pyplot as plt

#TODO: twitter.csv only has the last three weeks' worth of closing prices
def getClosingPrices():
    closingPrices = []
    with open("twitter.csv", newline='') as csvfile:
        closingPriceReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in closingPriceReader:
            print(row[0], row[4])
            if not row[4] == "Close":
                closingPrices.append(float(row[4]))
    closingPrices.reverse()
    return closingPrices

def parseArgs():
    closingPrices = getClosingPrices()
    dailyReturnRates = [None]*(len(closingPrices) - 1)
    for i in range(1, len(closingPrices)):
        dailyReturnRates[i - 1] = (closingPrices[i] - closingPrices[i-1]) 
        dailyReturnRates[i - 1] /= 0.5*(closingPrices[i] + closingPrices[i-1])
    muHat = np.mean(dailyReturnRates)
    sigmaHat = np.std(dailyReturnRates, ddof=1)
    paramNames = ["mu", "sigma", "T", "S", "X", "N", "n"]
    paramVals = [muHat, sigmaHat, 100, closingPrices[-1], 16, 1000, 30]
    for i in range(1, len(sys.argv)):
        paramVals[i - 1] = sys.argv[i]
    for i in range(len(paramNames)):
        print("The input value for", paramNames[i], "is:", paramVals[i])
    return paramVals

# simulates the path of a stock and outputs the estimated call and put prices
def simStock(mu, sigma, T, S, X, N, n):
    r = 0.01 # risk-free return rate
    dt = T/N
    calls, puts = [None]*n, [None]*n
    for path in range(n):
        pathPrice = [None] * N
        pathPrice[0] = S
        for j in range(N - 1):
            epsilon = np.random.normal()
            dS = pathPrice[j] * (mu*dt + sigma*epsilon*dt**0.5)
            pathPrice[j+1] = pathPrice[j] + dS
        #get the call and put price for this particular option
        calls[path] = np.exp(-1*r*T) * max(pathPrice[-1] - X, 0)
        puts[path] = np.exp(-1*r*T) * max(X - pathPrice[-1], 0)
        #plotting
        plt.plot(pathPrice)
    callPrice = np.mean(calls)
    putPrice = np.mean(puts)
    print("The optimal call price:", callPrice) 
    print("The optimal put price: ", putPrice)
    #opens the window that actually displays the plots on top of each other
    plt.show()

def main():
    paramVals = parseArgs()
    mu = float(paramVals[0]) # this stock's daily return rate
    sigma = float(paramVals[1]) # this stock's volatility
    T = int(paramVals[2]) # expiry date - time till expiration, in days
    S = float(paramVals[3]) # initial price? 
    X = float(paramVals[4]) # strike price
    N = int(paramVals[5]) # granularity
    n = int(paramVals[6]) # number of simulation paths

    simStock(mu, sigma, T, S, X, N, n)

if __name__ == '__main__':
    main()







