n=int(input())
# A조건
print(10000)

# B조건
cnt=0
divisors=[] # 약수
for i in range(1,n+1) :
    if n%i==0 :
        divisors.append(i)
divisors_set=set(divisors)
print(divisors)
for i in range(1,len(divisors)) : #target
    target=divisors[i]
    for j in range(i) :
        if target-divisors[j] in divisors_set :
            print(target, divisors[j])
            cnt+=1
            
            
print(cnt)
#조건 C -> 골드바흐의 증명
cnt=0
sieve=[True]*n
m=int(n**0.5)
for i in range(2,m+1) :
    if sieve[i] : # true
        for j in range(i+1, n, i) :
            sieve[j]=False
primes=[i for i in range(2, n) if sieve[i] == True]
# 어떤 수 +


# target을 찾자. 근데 소수 + 소수는 2를 사용하지 않는다면 짝수임. 따라서 홀수 소수 + 홀수 소수로 만들 수 있는 소수는 존재하지 않음.
# 따라서, 하나의 소수는 2로 고정됨.
primes_set=set(primes)
for target in primes : 
    if target-2 in primes_set :
        cnt+=1
print(cnt)




"""
divisors=[ i for i in range(1,int(n**0.5)+1) if n%i==0 ] 
divisors+=[n//i for i in divisors ]
divisors_set=set(divisors)
for divisor in divisors :
    if len(divisor)==1 : #제곱수
        val = divisor[0]
    else :
        min_val, max_val = divisor[0] , divisors[1]"""
        
# C조건 -> 에라토스테네스의 체

