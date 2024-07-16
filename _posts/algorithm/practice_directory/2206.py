import sys,math
from collections import deque

n,m=map(int,sys.stdin.readline().split())
matrix=[list(map(int,(sys.stdin.readline().strip()))) for _ in range(n)]
queue=deque()
visited=[[ [math.inf,math.inf] for _ in range(m)] for _ in range(n)]
visited[0][0][1]=1 #1은 뚫은 적이 없다 -> 남은 횟수가 1. 0은 뚫은 적이 있다->남은 횟수가 0.
queue.append((0,0,1)) #(pos_x, pos_y, 벽 뚫기 가능한 남은 횟수)
dx=[-1,0,1,0]
dy=[0,1,0,-1]

# 부서진 벽으로 왔을 때 
while queue :
    now_x , now_y, break_count = queue.popleft()
    #print("nx and ny " , now_x, now_y)
    if break_count==1 : # 남은 횟수가 1이라면 -> 벽 박살내는 것도 고려해야 한다. 근데 벽을 안 뚫어도 됨
        for i in range(4) : # 벽을 뚫고 간다
            next_x , next_y = now_x + dx[i] , now_y + dy[i]
            if next_x>=0 and next_x<n and next_y>=0 and next_y<m : #범위 밖이 아니면서
                if matrix[next_x][next_y]==1 and visited[next_x][next_y][0]==math.inf : # 벽 and 현재 간 것이 더 짧을 때 
                    queue.append((next_x, next_y, break_count-1))
                    visited[next_x][next_y][0]=visited[now_x][now_y][1]+1
    
    for i in range(4) : # 벽을 뚫지 않고 그냥 감
        next_x , next_y = now_x + dx[i] , now_y + dy[i]
        if next_x>=0 and next_x<n and next_y>=0 and next_y<m : # 범위 밖이 아니면서
            if matrix[next_x][next_y]==0 and visited[next_x][next_y][break_count] ==math.inf : # 현재 간 것이 더 짧을 때 
                queue.append((next_x, next_y, break_count))
                visited[next_x][next_y][break_count]=visited[now_x][now_y][break_count]+1

print(-1 if visited[n-1][m-1]==[math.inf, math.inf] else min(visited[n-1][m-1]) )
