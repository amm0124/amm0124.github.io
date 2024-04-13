# 처음 66 두 번째 77 세 번째 78퍼

n,start_x,start_y,dst_x,dst_y=map(int,input().split())
diff_x=dst_x-start_x
diff_y=dst_y-start_y
answer=-1
if diff_x>=0 and diff_y>=0 :
    if diff_x==0 and diff_y==0:
        answer="R"*n
    elif diff_x!=0 and diff_y==0: #x축 방향으로만 움직여야 한다면(R)
        answer="R"*n
    elif diff_x==0 and diff_y!=0 : #y축 방향으로만 움직여야 한다면
        if diff_y>n :
            answer="U"*n
        else : #diff_y<=n
            answer="U"*diff_y+"R"*(n-diff_y)
    else : # 두 방향으로 모두 움직여야 한다면
        if diff_x + diff_y <=n : # 한 바퀴안에 모든 것이 해결된다면
            answer="R"*diff_x + "U"*diff_y +"R"*(n-diff_x-diff_y)
        else : # 한 바퀴안에 해결되지 않는다면
            for i in range(1,n) :
                move_x=i
                move_y=n-i
                counting=min(diff_x//move_x, diff_y//move_y)
                remain_x=diff_x-(move_x)*counting  #remain_x=diff_x%move_x # x축으로 채워야 하는 거리
                remain_y=diff_y-(move_y)*counting  #remain_y=diff_y%move_y # y축으로 채워야 하는 거리
                if move_x-remain_x>=0 and move_y-remain_y>=0 :
                    tmp="R"*remain_x+"U"*remain_y+"R"*(move_x - remain_x) + "U"*(move_y - remain_y)   
                    if len(tmp)==n :           
                        if answer==(-1) : # R이 사전순으로 U보다 먼저 있음.
                            answer=tmp
                        else :
                            answer=min(answer,tmp)

print(answer)