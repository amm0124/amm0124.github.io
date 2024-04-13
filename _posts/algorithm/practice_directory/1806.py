import sys

n,target=map(int,sys.stdin.readline().split())
seq=list(map(int,sys.stdin.readline().split()))
#합이 s이상 제일 낮은 부분 수열 길이

if target>sum(seq) :
    print(0)
else :
    #seq_sum=[0 for _ in range(n+1)] #partial sum preprocessing
    s,e=0,0
    answer=n
    tmp=seq[0]
    while s<=n and e<=n :
        if tmp<target :
            e+=1
            if e==n :
                break
            tmp+=seq[e]
        else :
            tmp-=seq[s]
            answer=min(answer, e-s+1)

    print(answer)
        