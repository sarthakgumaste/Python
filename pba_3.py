
def rod_cutting(price, n):
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        for j in range(i):
            dp[i] = max(dp[i], price[j] + dp[i-j-1])

    return dp[n]


price = [2, 5, 7, 8, 10, 13, 17, 20]

n = int(input("Enter rod length: "))

max_profit = rod_cutting(price, n)

print("Maximum Profit:", max_profit)
