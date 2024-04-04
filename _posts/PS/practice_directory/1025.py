import sys

n,m=map(int,sys.stdin.readline().split())
matrix=[list(map(int, sys.stdin.readline().strip())) for _ in range(n)]
answer=-1

if n==1 and m==1 :
    if (matrix[0][0]**0.5)**2==matrix[0][0]:
        answer=matrix[0][0]
for row in range(n) :
    for col in range(m) :
        for row_step in range(-row, n-row) :
            for col_step in range(-col, m-col) :
                if row_step==0 and col_step==0 :
                    continue
                else :
                    tmp,pos_x,pos_y=0,row,col
                    while pos_x>=0 and pos_x<n and pos_y>=0 and pos_y<m :
                        tmp=10*tmp+matrix[pos_x][pos_y]
                        if int(tmp**0.5)**2==tmp :
                            answer=max(answer, tmp)   
                        pos_x+=row_step
                        pos_y+=col_step
                    
print(answer)

"""
입력:
5 5
22222
21002
20002
20002
22222
출력:
    
"""