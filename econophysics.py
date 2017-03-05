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
        paramVals[i - 1] = float(sys.argv[i])
    for i in range(len(paramNames)):
        print("The input value for", paramNames[i], "is:", paramVals[i])
    return paramVals

def main():
    paramVals = parseArgs()
    r = paramVals[0] # risk-free return rate
    sigma = paramVals[1] # volatility
    T = paramVals[2] # expiry date - time till expiration, in days
    S = paramVals[3] # initial price? TODO: idek
    X = paramVals[4] # strike price
    N = paramVals[5] # granularity
    n = paramVals[6] # number of simulation paths
    closingPrices = getClosingPrices()
    muHat = np.std(closingPrices)
    sigmaHat = np.std(closingPrices, ddof=1)

    for path in range(n):
        pathPrice = [S]
        dt = T/N
        for step in range(1, N):
            epsilon = np.random.normal()
            exponent = (r - 0.5*sigma**2)*dt + sigma * epsilon * dt**0.5
            pathPrice.append( pathPrice[-1]*np.exp(exponent) )

if __name__ == '__main__':
    main()







