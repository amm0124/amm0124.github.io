import sys
sys.setrecursionlimit(10**8)
def fib(n) :
    if n>=2 :
        if dp[n-1]==0 :
            dp[n-1]=fib(n-1)
        dp[n]=(dp[n-1][0]+dp[n-2][0], dp[n-1][1]+dp[n-2][1])
    return dp[n]

t=int(sys.stdin.readline())
dp=[0 for _ in range(41)]
dp[0]=(1,0)
dp[1]=(0,1)

for _ in range(t) :
    n=int(sys.stdin.readline())
    fib(n)
    print(dp[n][0], dp[n][1])