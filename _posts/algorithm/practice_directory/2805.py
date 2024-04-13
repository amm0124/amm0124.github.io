import sys 

n,m=map(int,sys.stdin.readline().split())
t=list(map(int,sys.stdin.readline().split()))
t.sort()

s=0 #s 높이로 자름
e=t[-1] #범위
answer=0
while s!=(e-1) :
    tmp=0
    cut=(s+e)//2
    tmp = sum(max(0, h - cut) for h in t)
    if tmp>=m : #m을 만들 수 있다면  
        s=cut
        answer=max(answer, cut)
    else : #m을 만들 수 없다면 
        e=cut

print(answer)