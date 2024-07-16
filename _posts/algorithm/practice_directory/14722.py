import sys

def return_prev(now) :
    if now==0 :
        return 2
    elif now==1 :
        return 0
    else : 
        return 1

n=int(input())
area = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
dp =[[-1*float("INF") for _ in range(n)] for _ in range(n)]

starts = []

for row in range(n) :
    for col in range(n) :
        if area[row][col]==0 :
            starts.append((row,col))

for start in starts :
    start_x, start_y = start[0], start[1]
    if dp[start_x][start_y]>1 :
        continue
    else : #dp[start_x][start_y]==0 or -float("INF") -> dp
        # 시작점이 방문하지 않은 상태임
        next = 1 # 다음은 초코 우유를 먹어야 함.
        flag=False
        for row in range(start_x, n) :
            for col in range(start_y, n) :
                if flag==True:
                    continue
                
                if row==start_x and col==start_y :
                    dp[row][col]=1
                else :
                    now = area[row][col] # 현재 우유
                    prev = return_prev(now) # 
                    if row==0 :
                        point = dp[row][col-1]+1 if area[row][col-1]==prev else dp[row][col-1] 
                        if dp[row][col]<=point : #탐색 진행
                            dp[row][col]=point
                        else :
                            flag=True
                    elif col==0 :
                        point = dp[row][col-1]+1 if area[row][col-1]==prev else dp[row][col-1] 
                        if dp[row][col]<=point : #탐색 진행
                            dp[row][col]=point
                        else :
                            flag=True
                    else :
                        point1 = 1+dp[row-1][col] if area[row-1][col]==prev else dp[row-1][col]
                        point2 = 1+dp[row][col-1] if area[row][col-1]==prev else dp[row][col-1]
                        
                        if dp[row][col]>point1 or dp[row][col]>point2:
                            flag=True
                        else :
                            dp[row][col]=max(point1,point2)
print(dp)
                
print(0 if dp[-1][-1]==-1*float("INF") else dp[-1][-1])