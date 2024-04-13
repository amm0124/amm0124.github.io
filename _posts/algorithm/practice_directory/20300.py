import sys

n=int(input())
t=list(map(int,sys.stdin.readline().split()))
t.sort()
answer=[]
if n%2==0 :
    answer=[t[i] + t[n-(i+1)] for i in range(n)]
    print(max(answer))
else :
    tmp=t[-1]
    tmp2=t[:-1]
    answer=[tmp2[i] + tmp2[(n-1)-(i+1)] for i in range(n-1)]
    print(max(max(answer) , tmp))