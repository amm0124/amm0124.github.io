n=int(input())
dp=[0 for _ in range(n+1)]
dp[1]=1/(n-1)

for i in range(2,n+1) : 
    dp[i]+=dp[i-1]*(1/(n-i+1))
print(dp)


from decimal import Decimal, getcontext
getcontext().prec = 12

dp = [0.0 for _ in range(n+1)]
dp[1] = Decimal(1.0) / Decimal(n-1)

for i in range(2, n):
    dp[i] = dp[i-1] + dp[i-1] * (Decimal(1.0) / Decimal(n-i+1))

print(float(dp[n-1]))