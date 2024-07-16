import sys
from collections import deque

n,m=map(int, sys.stdin.readline().split())
graph=[list(map(int, sys.stdin.readline().rstrip())) for _ in range(n)]
dx=[-1,0,1,0]
dy=[0,1,0,-1]
visited=[[0 for _ in range(m)] for _ in range(n)]
queue = deque()
queue.append((0,0))
visited[0][0]=1

while queue :
    pos_x, pos_y = queue.popleft()
    for i in range(4) :
        next_x=pos_x+dx[i]
        next_y=pos_y+dy[i]
        if next_x>=0 and next_x<n and next_y>=0 and next_y<m :
            if graph[next_x][next_y]==1 and visited[next_x][next_y]==0 :
                queue.append((next_x, next_y)) 
                visited[next_x][next_y]=visited[pos_x][pos_y]+1            

print(visited[-1][-1])