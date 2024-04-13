n=int(input())
sieve=[True]*n
m=int(n**0.5)

# 에라토스테네스의 체를 사용해서 O(n(log(logn)))으로 n이하의 소수 목록을 구했습니다.
for i in range(2,m+1) :
    if sieve[i]==True :
        for j in range(i+i, n, i) :
            sieve[j]=False
prime_dict=dict()
primes=[i for i in range(2, n) if sieve[i] == True]
len_=len(primes)

for i in range(len_) :
    for j in range(i,len_):
        if i+j<=1000000:
            if i+j not in prime_dict :
                prime_dict[i+j]=[i,j]
        else :
            break
answer=-1
for key in prime_dict.keys():
    target=n-key
    if target in prime_dict :
        answer=prime_dict[key]+prime_dict[target]
    
print(*answer, " ")