import sys
import numpy as np
import matplotlib.pyplot as plt

# simulates the path of a stock and outputs the estimated call and put prices
def simStock(r=0.01, mu=0.01, sigma=0.01, T=60, S=15, X=15, N=1000, n=30):
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
        plt.plot(pathPrice)
    callPrice = np.mean(calls)
    putPrice = np.mean(puts)
    print("Given that the option's strike price is %f and days till expiry is %i:"%(X,T))
    print("The optimal call price:", callPrice) 
    print("The optimal put price: ", putPrice)
    #opens the window that actually displays the plots on top of each other
    plt.xlabel("Day")
    plt.ylabel("Asset price (USD)")
    plt.show()

def main():
    r = float(input("Risk-free interest rate: "))
    mu = float(input("Asset's daily return rate: "))
    sigma = float(input("Volatility of asset: "))
    T = float(input("Days till this option's expiry date: "))
    S = float(input("Asset's current price: "))
    X = float(input("This option's strike price: "))
    N = int(input("Time steps per simulation: "))
    n = int(input("Number of simulation paths: "))
    simStock(r=r, mu=mu, sigma=sigma, T=T, S=S, X=X, N=N, n=n)

if __name__ == '__main__':
    main()







