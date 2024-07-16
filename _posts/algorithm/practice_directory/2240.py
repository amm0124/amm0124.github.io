import sys
t,w=map(int,sys.stdin.readline().split())
position=[0]+[int(input()) for _ in range(t)]

dp=[[0 for _ in range(w+1)] for _ in range(t+1)] 

for time in range(1,t+1) :
    dp[time][0]= dp[time-1][0]+(1 if position[time]==1 else 0)

for time in range(1,t+1) :
    for move in range(1,w+1) :
        now_position=position[time] # 과일 위치
        point = 1 if (now_position==1 and move%2==0) or (now_position==2 and move%2!=0) else 0
        #max(움직이지 않고 얻는 점수 , 움직여서 얻는 점수 )
        dp[time][move]=max(dp[time-1][move] , dp[time-1][move-1] )  + point
        
#print(dp)
print(max(dp[-1]))