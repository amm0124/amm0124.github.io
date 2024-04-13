import sys

n,c=map(int,sys.stdin.readline().split())
h=[int(sys.stdin.readline()) for _ in range(n)]
h.sort()
answer=0
for i in range(n) :
    if i==0 : 
        answer=max(answer,abs(h[0]-h[1]))
    elif i==(n-1) :
        answer=max(answer, abs(h[n-1]-h[n-2]))
    else :
        answer=max(answer, abs(h[i]-h[i-1]), abs(h[i]-h[i+1]))
    print("ANSWER : ", answer )
print(answer)