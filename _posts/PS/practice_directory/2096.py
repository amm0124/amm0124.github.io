import sys

n=int(input())
board=[]
dp_max, dp_min =[] , []
for i in range(n) :
    board=list(map(int,sys.stdin.readline().split()))
    if i==0 :
        dp_max=board[:]
        dp_min=board[:]
    else:
        zero, one, two = dp_max[0], dp_max[1], dp_max[2]
        dp_max[0]=max(zero, one)+board[0] 
        dp_max[1]=max([zero, one, two])+board[1] 
        dp_max[2]=max(one, two)+board[2] 
        zero, one, two = dp_min[0], dp_min[1], dp_min[2]
        dp_min[0]=min(zero, one)+board[0] 
        dp_min[1]=min([zero, one, two])+board[1] 
        dp_min[2]=min(one, two)+board[2] 
    
    
print(max(dp_max))
print(min(dp_min))       
"""boards=[list(map(int, sys.stdin.readline().split())) for _ in range(n)]
max_dp=[boards[0], boards[1], boards[2]]
min_dp=[boards[0], boards[1], boards[2]]

#dp=[[0 for _ in range(n)] for _ in range(n)]
for board in boards[1:]:
    pass"""