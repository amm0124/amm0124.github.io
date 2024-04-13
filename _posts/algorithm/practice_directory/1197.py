import sys

v,e=map(int,sys.stdin.readline().split())
weight_list=[0 for _ in range(e)]
mst_set=[]
for i in range(e) :
    a,b,c=map(int,sys.stdin.readline().split())
    weight_list[i]=(c,a,b)
weight_list.sort() # sorting

#making_mst
answer=0
for weights in weight_list:
    node_a=weights[1]
    node_b=weights[2]
    weight=weights[0] #a -> b weight 
    