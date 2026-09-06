a = input("Enter first sequence: ")
b = input("Enter second sequence: ")

m = len(a)
n = len(b)

dp = [[0] * (n + 1) for i in range(m + 1)]

for i in range(1, m + 1):
    for j in range(1, n + 1):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

i = m
j = n
lcs = ""

while i > 0 and j > 0:
    if a[i - 1] == b[j - 1]:
        lcs = a[i - 1] + lcs
        i = i - 1
        j = j - 1
    elif dp[i - 1][j] > dp[i][j - 1]:
        i = i - 1
    else:
        j = j - 1

print("The common subsequence is:", lcs)
print("Length of LCS =", dp[m][n])