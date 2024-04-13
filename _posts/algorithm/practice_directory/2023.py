def is_prime(n) :
    if n&1==1 : #홀수라면
        for i in range(3,int(n**0.5)+1) :
            if n%i==0:
                return False
        return True
    else : #짝수라면
        return False

n=int(input())
primes=[2,3,5,7]
ends=[1,3,7,9]
# 끝 자리가 1 3 7 9 입니다.
cnt=1
while cnt!=n :
    new_primes=[]
    for prime in primes :
        for end in ends :
            if is_prime(prime*10+end) :
                new_primes.append(10*prime+end)
    primes=new_primes
    cnt+=1
for prime in primes :
    print(prime)