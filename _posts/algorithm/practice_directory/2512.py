import sys
n=int(input())
budgets=list(map(int, sys.stdin.readline().split()))
m=int(sys.stdin.readline())
budgets.sort()
answer=0
if m>=sum(budgets) :
    print(max(budgets))
else : #아닌 경우 직접 찾기
    s=1
    e=budgets[-1]
    while s<=e :
        mid=(s+e)//2 #상한액 
        tmp=0
        for budget in budgets :
            tmp+=min(mid,budget)
        if m>=tmp : #총 예산이  
            s=mid+1
            answer=max(answer, mid)
        else :
            e=mid-1
    print(answer)