n=int(input())
answer=[] # (x,y) 순서쌍
count=0 # 횟수
for i in range(int(n//5)+1) : #i는 5를 사용한 횟수입니다.
    x=n-5*i
    if x%2==0 :
        answer.append((x//2,i))
        count+=1
        
if n==0 or count==0 :
    print("XXX")
else:       
    print(f"pair is {answer}, count is {count}") 