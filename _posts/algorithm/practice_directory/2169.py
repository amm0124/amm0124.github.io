import sys

n,m=map(int, sys.stdin.readline().split())
board=[list(map(int, sys.stdin.readline().split())) for _ in range(n)]
dp=[[0 for _ in range(m)] for _ in range(n)]

dp[0][0]=board[0][0]
dx=[0,0]
dy=[-1,1]

for col in range(1,m):
    dp[0][col]=dp[0][col-1]+board[0][col]
    
for row in range(1,n) :
    # 위로 내려온 케이스
    for col in range(m) :
        dp[row][col]=dp[row-1][col]+board[row][col]
    print(dp[row])
    # 오른쪽으로 만난 경우
    for col in range(1,m) :
        if dp[row][col] < dp[row][col-1] + board[row][col]:
            dp[row][col]=dp[row][col-1] + board[row][col]
    print(dp[row])
    for col in range(m-2,-1,-1) :
        if dp[row][col] < dp[row][col+1]+ board[row][col]:
            dp[row][col]=dp[row][col+1]+ board[row][col]
    print(dp[row])
    print("-----------------------")
print(dp)
print(dp[n-1][m-1])