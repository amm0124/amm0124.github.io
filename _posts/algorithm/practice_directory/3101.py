import sys

n,k=map(int, sys.stdin.readline().split())
jump=sys.stdin.readline().strip()
index={'U':0 ,'R':1, 'D':2, 'L':3}
pos_x,pos_y = 1,1
bundle=[1 for _ in range(2*n)] # 1, 2, 3, ...2n-1까지 시작점의 숫자 저장
diff=1

for i in range(2,n+1) :
    bundle[i]=bundle[i-1]+diff
    diff+=1
  
for i in range(n+1, 2*n) :
    bundle[i]=bundle[i-1]+diff
    diff-=1
    
print(bundle)
# U R D L
dx=[-1,0,1,0]
dy=[0,1,0,-1]
answer=1
now=1
for i in range(k) :
    char=jump[i]
    next_x, next_y=pos_x+dx[index[char]], pos_y+dy[index[char]]
    sum_=next_x+next_y
    b=sum_-1
    if b<=n : #1~n번째 묶음
        if b&1==1 : #홀수번째 묶음 
            start_x=1
            start_y=b
        else : #짝수번째 묶음
            start_x=b
            start_y=1
        answer+= bundle[b] + abs(next_x-start_x)+abs(next_y-start_y)
    else : #n+1 ~ 2n-1번쨰 묶음
        pass
    
    
        
    pos_x=next_x
    pos_y=next_y
    print("ans: ",answer)
    
