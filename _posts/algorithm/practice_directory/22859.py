import sys

doc=sys.stdin.readline().strip()[6:-7] #<main> parsing
doc=doc.split('</div>')[:-1] #</div> 기준으로 parsing -> 맨 마지막 ''는 무시하면 됨.->[:-1]
print("start!!------------------")
print("div parsing result : " ,doc)
print("------------------------")
for d in doc : #d 내부 p들을 parsing해야 함.
    p_parsing=d.split("<p>")
    print("title : "+p_parsing[0][12:-2]) #div title parsing
    #print("<p> parsing result : " , p_parsing)
    for i in range(1, len(p_parsing)) : #0번은 div title입니다.
        parser=p_parsing[i][:-4].strip() # p_parsing[i][:-4]를 사용해서 </p>를 제거합니다. 
        print(parser)
        #이후, <br> , <i> , <b> 를parsing합니다.



