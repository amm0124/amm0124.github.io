import sys
sys.setrecursionlimit(10**9)


n=int(input())
scv=list(map(int, sys.stdin.readline().split()))+[0 for _ in range(3-n)]

#[공격횟수][scv][scv][scv]
dp=[ [ [ [0 for _ in range(scv[0]+1)] for _ in range(scv[1]+1)] for _ in range(scv[2]+1)] for _ in range(20)]
dp[0][scv[0]][scv[1]][scv[2]]=1 