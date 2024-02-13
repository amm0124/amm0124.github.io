import sys

n,k=map(int,sys.stdin.readline().split()) #물건 수, 제한
dp=[[0 for _ in range(k+1)] for _ in range(n+1)]
answer=0
for i in range(1,n+1) :
    w,v = map(int,sys.stdin.readline().split()) #weight, value
    for j in range(1,k+1) :
        if j>=w :
            dp[i][j] = max(dp[i-1][j], dp[i-1][j-w] + v)
        else :
            dp[i][j] = dp[i-1][j]
    print(dp[i], f"{i}번째 item의 dp table")

print(dp[n][k]) 