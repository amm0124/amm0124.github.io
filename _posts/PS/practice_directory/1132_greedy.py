import sys
weight=dict()
n=int(input())
arr=[sys.stdin.readline().strip() for _ in range(n)]

for string in arr :
    len_=len(string)
    if len_==1 :
        continue
    for i,char in enumerate(string) :
        if char not in weight :
            weight[char]=(10**(len_ - (i+1)))
        else :
            weight[char]+=(10**(len_ - (i+1)))

sorted_weight=sorted(weight.items(), key=lambda x : x[1], reverse=True)
print(sorted_weight)
answer=0
max_num=9
for item in sorted_weight :
    answer+=item[1]*max_num
    max_num-=1  
    print(answer)