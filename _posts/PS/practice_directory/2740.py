import sys

n,m=map(int,sys.stdin.readline().split())
mat1=[list(map(int,sys.stdin.readline().split())) for _ in range(n)]
n,m=map(int,sys.stdin.readline().split())
mat2=[list(map(int,sys.stdin.readline().split())) for _ in range(n)]
result =  [  [sum([mat1[row][tmp]*mat2[tmp][col] for tmp in range(len(mat2))] )  for col in range(len(mat2[0]))] for row in range(len(mat1))  ]
for row in result :
    print(*row)


