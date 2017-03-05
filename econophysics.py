import sys
import numpy as np
import csv

#TODO: twitter.csv only has the last three weeks' worth of closing prices
def getClosingPrices():
    closingPrices = []
    with open("twitter.csv", newline='') as csvfile:
        closingPriceReader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in closingPriceReader:
            # print(row[0])
            if not row[4] == "Close":
                closingPrices.append(float(row[4]))
    closingPrices.reverse()
    return closingPrices

def parseArgs():
    paramNames = ["r", "sigma", "T", "S", "X", "N", "n"]
    paramVals = [0.1, 0.5, 100, 15, 16, 1000, 30]
    for i in range(1, len(sys.argv)):
        paramVals[i - 1] = sys.argv[i]
    for i in range(len(paramNames)):
        print("The input value for", paramNames[i], "is:", paramVals[i])
    return paramVals

def main():
    paramVals = parseArgs()
    r = float(paramVals[0]) # risk-free return rate
    sigma = float(paramVals[1]) # volatility
    T = int(paramVals[2]) # expiry date - time till expiration, in days
    S = float(paramVals[3]) # initial price? TODO: idek
    X = float(paramVals[4]) # strike price
    N = int(paramVals[5]) # granularity
    n = int(paramVals[6]) # number of simulation paths
    closingPrices = getClosingPrices()
    muHat = np.std(closingPrices)
    sigmaHat = np.std(closingPrices, ddof=1)

    dt = T/N
    calls, puts = [None]*n, [None]*n
    for path in range(n):
        pathPrice = [None] * N
        pathPrice[0] = S
        
        for j in range(N - 1):
            epsilon = np.random.normal()
            exponent = (r - 0.5*sigma**2)*dt + sigma * epsilon * dt**0.5
            pathPrice[j+1] = pathPrice[j]*np.exp(exponent) 
        calls[path] = np.exp(-1*r*T) * max(pathPrice[-1] - X, 0)
        puts[path] = np.exp(-1*r*T) * max(X - pathPrice[-1], 0)
    callPrice = np.mean(calls)
    putPrice = np.mean(puts)
    print(callPrice, putPrice)

if __name__ == '__main__':
    main()







