import sys
from collections import deque
m,n,h=map(int,sys.stdin.readline().split())
sum_=0
tomato=[[[0 for _ in range(h)] for _ in range(n)] for _ in range(m)] #[가로][세로][높이]
#세로 가로 높이 순으로 list comprehensive를 통해서 만들어도 됨.
flag = True
sum_=0
for k in range(h) :
    for j in range(n) :
        t=list(map(int,sys.stdin.readline().split()))
        for i in range(len(t)) :
            tomato[i][j][k]=t[i]
            if t[i]==0 :
                flag =False 
            elif t[i]==1 :
                sum_+=1
if flag and sum_>=1: #토마토가 모두 익어있는 경우 -> 0이 하나라도 없는 경우
    print(0)
else :
    queue=deque()
    for i in range(m) :
        for j in range(n) :
            for k in range(h) :
                if tomato[i][j][k]==1 :
                    queue.append((i,j,k))
    diff=[(-1,0,0) , (0,1,0) , (1,0,0) , (0,-1,0) , (0,0,1) , (0,0,-1)]
    while queue :
        pos_x, pos_y, pos_z= queue.popleft()
        for i in range(6) :
            next_x=pos_x+diff[i][0]
            next_y=pos_y+diff[i][1]
            next_z=pos_z+diff[i][2]
            if 0<=next_x<m and 0<=next_y<n and 0<=next_z<h :
                if tomato[next_x][next_y][next_z]==0:
                    tomato[next_x][next_y][next_z]=tomato[pos_x][pos_y][pos_z]+1
                    queue.append((next_x, next_y, next_z))
                    
    flag=True
    answer=0
    for i in range(m) :
        for j in range(n) :
            for k in range(h) :
                if tomato[i][j][k]==0 : #모든 토마토 못 익음
                    flag=False
                answer=max(answer, tomato[i][j][k])
    
    if flag :
        print(answer-1)
    else :
        print(-1)      
       
                        
        
