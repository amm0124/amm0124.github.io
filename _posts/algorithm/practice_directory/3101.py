import sys

n,k=map(int, sys.stdin.readline().split())
jump=sys.stdin.readline().rstrip()
index={'U':0 ,'R':1, 'D':2, 'L':3}
pos_x, pos_y=1,1

bundle=[0 for _ in range(2*n)] # 1, 2, 3, ...2n-1까지 시작점을 


# U R D L
dx=[-1,0,1,0]
dy=[0,1,0,-1]
answer=1
for i in range(k) :
    char=jump[i]
    next_x, next_y=pos_x+dx[index[char]], pos_y+dy[index[char]]
    sum_=next_x+next_y
    
    start=1+((sum_-1)*(sum_-2))//2
    end=((sum_)*(sum_-1))//2
    
    if sum_%2==0: #짝수, 우상향
        answer+=((next_y)-1)+(start)
    else: #홀수, 우하향
        answer+=(next_x)-1+start
    
    print("ans: ",answer)
    
"""if char=='U' :
    pass
elif char=='R':
    pass
elif char=='D':
    pass
else : #char=='R'
    pass"""