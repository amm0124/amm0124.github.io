import sys
from collections import deque

n,m,k=map(int,sys.stdin.readline().split())
board=["0" if i==0 else "0"+sys.stdin.readline().strip() for i in range(n+1)] # padding 추가
dp=[[[False,False] for _ in range(m+1)] for _ in range(n+1)] #dp[row][col][0] -> visited, [1] -> dp
q=int(sys.stdin.readline())

dx=[-1,0]+[(-1)*i for i in range(1, k+1)]
dy=[0,-1]+[(-1)*i for i in range(1, k+1)]
queue=deque()
queue.append((n,m))
dp[n][m][0], dp[n][m][1]= True , False # 방문은 True, 도달하면 실패 
while queue:
    pos_x, pos_y = queue.popleft()
    sol=dp[pos_x][pos_y][1] #sol에는 pos_x, pos_y에 가면 이길 수 있는지 아닌지 값이 저장되어 있다.
    for i in range(2+k) :
        next_x, next_y = pos_x+dx[i], pos_y+dy[i]
        if next_x>=1 and next_x<=n and next_y>=1 and next_y<=m : #board 내부에 
            if board[next_x][next_y]!='#' and not dp[next_x][next_y][0]: # 막혀있지 않고 방문하지 않았다면
                dp[next_x][next_y][0]=True # 방문 처리
                if not dp[next_x][next_y][1] :
                    dp[next_x][next_y][1] = not sol
                queue.append((next_x, next_y))
        
for _ in range(q) :
    x,y=map(int,sys.stdin.readline().split())
    if dp[x][y][1] : 
        print("First")
    else :
        print("Second")