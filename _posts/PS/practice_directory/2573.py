import sys
from collections import deque

n,m=map(int, sys.stdin.readline().split())
graph=[list(map(int, sys.stdin.readline().split())) for _ in range(n)]
dx=[-1,0,1,0]
dy=[0,1,0,-1]
answer=0

while True : 
    answer+=1
    count=[[0 for _ in range(m)] for _ in range(n)] #visited and count, -1이 아니라면 방문한 곳임.
    for row in range(n) :
        for col in range(m) :
            if graph[row][col]!=0:
                zero=0
                for i in range(4) :
                    next_x=row+dx[i]
                    next_y=col+dy[i]
                    if (next_x>=0 and next_x<n) and (next_y>=0 and next_y<m) :
                        if graph[next_x][next_y]==0 :
                            zero+=1
                count[row][col]=zero
        
    for row in range(n) :
        for col in range(m) :
            if graph[row][col]!=0 :
                graph[row][col]=max(0, graph[row][col]-count[row][col])
    
    visited=[[False for _ in range(m)] for _ in range(n)]
    #chunk 수 구하기  
    chunk=0      
    for row in range(n) :
        for col in range(m) :         
            if graph[row][col]!=0 and not visited[row][col]: 
                queue=deque()
                queue.append((row,col))
                visited[row][col]=True
                chunk+=1
                while queue : #bfs
                    pos_x, pos_y= queue.popleft()
                    for i in range(4) :
                        next_x=pos_x+dx[i]
                        next_y=pos_y+dy[i]
                        if (next_x>=0 and next_x<n) and (next_y>=0 and next_y<m) : # and visited[next_x][next_y]==(-1)
                            if graph[next_x][next_y]!=0 and not visited[next_x][next_y] :
                                queue.append((next_x, next_y))
                                visited[next_x][next_y]=True
    if chunk==0 :
        print(0)
        break
    elif chunk>=2 :
        print(answer)
        break