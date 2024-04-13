import sys
n,k=map(int,sys.stdin.readline().split())
dp=[0 for _ in range(k+1) ]
coins=[int(sys.stdin.readline()) for _ in range(n)]
dp[0]=1

for coin in coins :
    for target in range(coin, k+1) : 
        if target-coin>=0 :
            dp[target]+=dp[target-coin]
print(dp)

    
