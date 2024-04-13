import sys

n=int(input())
tiles=list(map(int, sys.stdin.readline().split()))  
answer=0
# index_diff는 tiles의 value를 key로 가지고, index를 value로 가짐 
# 이를 통해, 다음 타일이 있는지 상수 시간 접근 가능
# index_dict로 썼어야 하는데, diff로 써버렸습니다;;
index_diff=dict() 
for i in range(n) :
    index_diff[tiles[i]]=i 

for row in range(n) :
    for col in range(row+1,n) :
        s=tiles[row] # 시작
        e=tiles[col] # 끝
        diff=e-s # 간격
        depth, tmp = 2, s+e # depth : 시작 , 끝을 갔으므로 2칸 갔다는 의미입니다. tmp는 합계 저장.
        while True : #while문을 사용해서 dict를 순회합니다. 
            if e+diff not in index_diff : # 현재 타일에서 다음 타일이 존재하지 않는다면 멈춤.
                break
            else : # 다음에 갈 수 있는 타일이 있다면 다음 타일로 갑니다.
                e+=diff
                tmp+=e
                depth+=1      
        if depth>=3 : #최종적으로 존재한다면 
            answer=max(answer,tmp)
           
print(answer)