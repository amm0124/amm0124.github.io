from itertools import permutations

target=int(input())
m=int(input())
breakdown=list(map(int, input().split()))
remote_control = set([str(i) for i in range(10) if i not in breakdown]) # 쓸 수 있는 버튼 
print(remote_control)
answer=min( abs(target-100), 100+(500000-target) ) # 단방향으로 갈 수 있는 최대
answer=0
for num in range(500001) :
    num=str(num)
    flag=True
    for n in num :
        if n in remote_control :
            flag=False
    if flag : #만들 수 있는 숫자라면
        if num>=target :
            tmp=min(target-int(num), )
            answer=min(answer, )
        
    



if target >= 100 :
    answer=min(target-100 , 100 + 500000-target)
else :
    answer=100-target


