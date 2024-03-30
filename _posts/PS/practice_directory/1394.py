import sys,math
inp=sys.stdin.readline().strip()
target=sys.stdin.readline().strip()
answer=0
for i in range(len(inp)) :
    if inp[i]==target[-1]:
        answer=i+1

answer+=(math.pow(len(inp),len(target)-1))%900528
print(int(answer%900528))


"""
    i번째를 알고 싶으면
    math.pow(use_code_len,i-1)+use_code에서 해당하는 알파벳의 index
    
    """