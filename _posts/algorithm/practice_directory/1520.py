import sys
n,m=map(int, sys.stdin.readline().split())
board=[list(map(int, sys.stdin.readline().split())) for _ in range(n)]
dp=[[0 for _ in range(m)] for _ in range(n)]

#dp[row][col]를 알기 위해선 위, 오른쪽, 왼쪽 다 알아야 함.
dp[0][0]=1
dx=[0,0]
dy=[-1,1]

for col in range(1,m):
    if board[0][col-1] > board[0][col] :
        dp[0][col]=dp[0][col-1] # 초깃값 설정

for row in range(1,n) :
    for col in range(m) :
        if board[row][col] < board[row-1][col] :
            dp[row][col]=dp[row-1][col] # 이 때, 최소 아래로만 갔을 때 반영되어 있음.
     
    for col in range(1,m) :
        if board[row][col] < board[row][col-1] : 
            dp[row][col]+=dp[row][col-1]
     
    for col in range(m-2,-1,-1) :
        if board[row][col] < board[row][col+1] : 
            dp[row][col]+=dp[row][col+1]
     
print(dp)
print(dp[n-1][m-1])       
        