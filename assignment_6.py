def top_down(weights, values, n, capacity, dp):
    if n == 0 or capacity == 0:
        return 0

    if dp[n][capacity] != -1:
        return dp[n][capacity]

    if weights[n - 1] <= capacity:
        dp[n][capacity] = max(
            values[n - 1] + top_down(weights, values, n - 1, capacity - weights[n - 1], dp),
            top_down(weights, values, n - 1, capacity, dp)
        )
    else:
        dp[n][capacity] = top_down(weights, values, n - 1, capacity, dp)

    return dp[n][capacity]


def bottom_up(weights, values, n, capacity):
    dp = [[0] * (capacity + 1) for i in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


n = int(input("Enter number of items: "))

weights = []
values = []

for i in range(n):
    w = int(input("Enter weight of item " + str(i + 1) + ": "))
    v = int(input("Enter value of item " + str(i + 1) + ": "))
    weights.append(w)
    values.append(v)

capacity = int(input("Enter maximum weight: "))

dp = [[-1] * (capacity + 1) for i in range(n + 1)]

print("Maximum value using Top-Down:", top_down(weights, values, n, capacity, dp))
print("Maximum value using Bottom-Up:", bottom_up(weights, values, n, capacity))