import sys

# 위 쪽 공청기 - right 
def ccw_circular():
    global r,c,room,cleaner
    cleaner_x, cleaner_y = cleaner[0][0], cleaner[0][1]

    
    

# 아래 쪽 공청기 - left
def cw_circular():
    global r,c,room,cleaner
    cleaner_x, cleaner_y = cleaner[1][0], cleaner[1][1]
    # 문제 x
    for new_ in range(cleaner_x-2,-1,-1) :
        room[new_+1][cleaner_y]=cleaner[new_][cleaner_y] 
    # ?
    for new_ in range(1,c) :
        room[0][new_-1]=room[0][new_]

    # 
    for new_ in range(1,cleaner_x+1) :
        room[new_-1][c-1]=room[new_][c-1]

    for new_ in range(c-2,0,-1) :
        room[cleaner_x][new_+1] = room[cleaner_x][new_]
    
    print(*room,end='\n')
    
r,c,t=map(int,sys.stdin.readline().split())
room = [list(map(int,sys.stdin.readline().split())) for _ in range(r)]
dx=[-1,0,1,0]
dy=[0,1,0,-1]
cleaner=[]

for row in range(r) :
    for col in range(c) :
        if room[row][col]==-1 :
            cleaner.append((row,col)) # 위 , 아래 순으로
            
            
cw_circular()
"""

for time in range(t) :
    for row in range(r) :
        for col in range(c) :
            # 확산
            if room[row][col]!=0 :
                cnt=0
                for i in range(4) :
                    next_x=row+dx[i]
                    next_y=col+dy[i]
                    if next_x>=0 and next_x<r and next_y>=0 and next_y<c :
                        if room[next_x][next_y]!=(-1): #공기청정기 
                            room[next_x][next_y]+=int(room[row][col]//5)   
                            cnt+=1
                room[row][col]-=(cnt)*int(room[row][col]//5)
            # 공기청정기         
            ccw_circular()
            cw_circular()
                

"""