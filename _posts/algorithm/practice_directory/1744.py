n=int(input())
neg , pos , ans = [] , [] , 0
for _ in range(n) :
    tmp =int(input())
    if tmp <= 0 :
        neg.append(tmp)
    else :
        pos.append(tmp)
neg.sort() ; pos.sort()

for i in range(len(neg)//2) :
    ans+= neg[i]*neg[i+1] if neg[i]*neg[i+1] else neg[i]+neg[i+1]
if len(neg)&1==1 :
    ans+=neg[-1]
    
for i in range(len(pos)//2) :
    ans+= pos[i]*pos[i+1] if pos[i]*pos[i+1] else pos[i]+pos[i+1]