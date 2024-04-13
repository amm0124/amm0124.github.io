import sys
n=int(input())
weights=list(map(int,sys.stdin.readline().split()))
weights.sort()

if weights[0]!=1 :
    print(1)
else : #일단 1은 만들 수 있음.
    prev=1 #1~prev까지는 무조건 만들 수 있음.
    for i in range(1,n) :
        if weights[i]-prev<=1 :
            prev+=weights[i]
        else :
            print(prev+1)
            sys.exit()
    print(sum(weights)+1)
    """
    일단 같거나, +1씩 커져야 함.
    그게 아니라면 기존에 구한 x까지는 가능함. 
    now가 x+1, x라면 x=x+now가 됨.
    아니라면 즉 2이상 차이가 나버리면 그 사이 붕 뜬 구간이 존재하므로 할 수 없다.
    
    
    
    """