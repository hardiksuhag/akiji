import math
def search(name_list, name_searched, count):
    def dist(a,b,i):
        p1=i
        p2=i
        b1=False
        b2=False
        while(0<=p1<len(b)):
            if(a[i]==b[p1]):
                break
            p1-=1
        while(0<=p2<len(b)):
            if(a[i]==b[p2]):
                break
            p2+=1
        b1=(0<=p1<len(b))
        b2=(0<=p2<len(b))
        if(b1 and b2):
            return(min(abs(p1-i),abs(p2-i)))
        elif(b1 and (not b2)):
            return(abs(p1-i))
        elif((not b1) and b2):
            return(abs(p2-i))
        else:
            return(-1)
    def f(x):
        smth=(math.e)**(x)
        return((smth)/((1+smth)**2))
    def score(test_name_taken):
        test_names_all=test_name_taken.split('.')
        scr_final=0
        for test_name in test_names_all:
            a=[]
            b=[]
            a.extend(name_searched.lower())
            b.extend(test_name.lower())
            scr=0
            for i in range(len(a)):
                d=dist(a,b,i)
                if(d==-1):
                    continue
                else:
                    scr+=f(d)
            scr/=len(a)
            scr_final=max(scr_final,scr)
        return(scr_final)
    name_list.sort(key=score)
    name_list.reverse()
    return(name_list[0:count])

