import sys

n=int(input())
answer=0
places=list(map(int,sys.stdin.readline().split()))
p_sum=[0 for _ in range(n+1)]
p_sum[1]=places[0] # 잘못한 부분
for i in range(2,n+1) :
    p_sum[i]=p_sum[i-1]+places[i-1]
# p_sum[j+1]-p_sum[i]로 i~j까지 합을 바로 구할 수 있게 되었습니다.

# case1 : 벌이 제일 왼쪽 끝(0)에 있을 때 -> 꿀통의 위치는 제일 오른쪽 끝(n-1)에 있어야 합니다.
for bee2 in range(1,n-1) :
    answer=max(answer, p_sum[bee2]-p_sum[1] + 2*(p_sum[n]-p_sum[bee2+1]))

# case2 : 벌이 제일 오른쪽 끝(n-1)에 있을 때 -> 꿀통의 위치는 제일 왼쪽 끝(0)에 있어야 합니다.
for bee2 in range(1,n-1) :
    answer=max(answer, p_sum[n-1]-p_sum[bee2+1] + 2*(p_sum[bee2]-p_sum[0]))

# case3 : 꿀통이 가운데 있다면 양 끝을 봅니다.
for honeypot in range(1,n-1) :
    answer=max(answer, (p_sum[honeypot+1]-p_sum[1])+(p_sum[n-1]-p_sum[honeypot])  )
print(answer)