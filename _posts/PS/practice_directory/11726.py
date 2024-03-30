n=int(input())
dp=[_ for _ in range(n+1)]
for i in range(3,n+1) : dp[i]=(dp[i-1]+dp[i-2])%10007
print(dp[n])