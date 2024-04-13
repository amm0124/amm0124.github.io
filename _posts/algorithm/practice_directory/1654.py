import sys
k,n=map(int, sys.stdin.readline().split())
lans=[int(sys.stdin.readline()) for _ in range(k)]
#n개 이상의 랜선 만들기
lans.sort()
s=1
e=lans[-1]
answer=0
while s<=e :
    cut=(s+e)//2
    tmp=0
    if cut==0 :
        pass
        
    else :
        for lan in lans :
            tmp+=max(0, lan//cut)
        if tmp>=n: #cut을 키워도 됨
            answer=max(answer, cut)
            s=cut+1
        else :
            e=cut-1
print(answer)

