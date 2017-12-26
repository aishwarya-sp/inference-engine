import pdb
import time
def isConstant(str):
    return str[0].isupper()
    
def standardize(s,i):
    #pdb.set_trace()
    s = s.replace(" ","")
    dict = {}
    temp = s 
    temp = temp.split("|")
    for j in temp:
        j = j.split("(")
        j = j[1]
        j = j.replace(")","")
        j = j.split(",")
        for k in j:
            if k[0].islower():
                dict[k] = k+str(i)
    for item in dict:
        s = s.replace("("+item+"," ,"("+ dict[item]+",")
        s = s.replace(","+item+"," ,","+ dict[item]+",")
        s = s.replace(","+item+")" ,","+ dict[item]+")")
        s = s.replace("("+item+")" ,"("+ dict[item]+")")

        
    return s 
        
 
    
def unify(str1,str2,p):
    print str1,str2,p
    #pdb.set_trace()
    #print Kb
    #print Kb_pred
    #print str1,str2,p
    temp = p
    if p[0] == "~":
        p = p[1:]
    dict = {}
    lit1 = str1.split("|")
    lit2 = str2.split("|")
    #print lit1 , lit2
    for i in lit1:
        if temp in i:
            p1 = i
            c = i.split("(")[0]
            if c[0] == "~":
                c1 = c[1:]
            else:
                c1 = "~" + c
            l1 = i.split("(")[1] 
    
    for j in lit2:
        if c1 in j:
            p2 = j
            l2 = j.split("(")[1]
    #if p1 in loop:
        #return "loop"
    print p,c
    l1 = l1.replace(")","")
    l1 = l1.split(",")
    l2 = l2.replace(")","")
    l2 = l2.split(",")
    zipped = zip(l1,l2)
    for item in zipped: 
        item = list(item)
        item[0] = item[0].replace(" ","")
        item[1] = item[1].replace(" ","")
        if item[0] == item[1]:
            pass
        else:
            v1 = isConstant(item[0])
            v2 = isConstant(item[1])
            if v1 is True and v2 is True:
                if not (item[0] == item[1]):
                    return "Cannot Unify"
            if v1 is True and v2 is False:
                if item[1] in dict:
                    return "Cannot Unify"
                else:
                    dict[item[1]] = item[0]
            if v1 is False and v2 is True:
                if item[0] in dict:
                    return "Cannot Unify"
                else:
                    dict[item[0]] = item[1]
            if v1 is False and v2 is False:
                if item[1] in dict:
                    return "Cannot Unify"
                else:
                    dict[item[1]] = item[0]
           
    newstr = ""
    if not len(lit1) is 0:
        for l in lit1:
            if l == p1:
                pass
            else:
                newstr = newstr + l + "|"
    if not len(lit2) is 0:
        for l in lit2:
            if l == p2:
                pass
            else:
                newstr = newstr + l + "|"
            
    newstr = newstr[:-1]
    for i in dict:
        p1 = p1.replace("("+i+",","("+dict[i]+",") 
        p1 = p1.replace(","+i+",",","+dict[i]+",")
        p1 = p1.replace(","+i+")",","+dict[i]+")")
        p1 = p1.replace("("+i+")","("+dict[i]+")") 
        
        newstr = newstr.replace("("+i+",","("+dict[i]+",") 
        newstr = newstr.replace(","+i+",",","+dict[i]+",")
        newstr = newstr.replace(","+i+")",","+dict[i]+")")
        newstr = newstr.replace("("+i+")","("+dict[i]+")")  
    loop.add(p1)
    #print loop
    return newstr
                 
def getLiteral(query,p):
    #pdb.set_trace()
    query = query.replace(" ","")
    lit1 = query.split("|")
    if p[0] == "~":
        p = p[1:]
    for i in lit1:
        if p in i:
            p1 = i
    return p1

def getPredicates(query):
    pred = []
    str = query 
    str = str.replace(" ","")
    lit = str.split("|")
    for l in lit:
        if not (l == ""):
            elements = l.split("(")
            p = elements[0]
            pred.append(p)
    return list(pred)


def findPredicate(p1):
    if p1 in Kb_pred:
        if len(Kb_pred[p1]) is 0:
            #print p1, Kb_pred[p1]
            return -1
        else:
            return Kb_pred[p1]
    return -1


   
def resolve(query):
    stop = time.time()
    if stop - start > 15:
        return False
    #pdb.set_trace()
    query = query.replace(" ","")
    if len(query) == 0:
        return True
    if query == first_string:
        return False
    pred = getPredicates(query)
    for p in pred:
        if p[0] == "~":
            p1 = p[1:]
        else:
            p1 = "~" + p
        index = findPredicate(p1)
        if (index < 0):
            return False
        else:
            for i in index:
                lit = getLiteral(query,p)
                if lit in loop:
                    return False
                q1 = unify(query,Kb[i],p)
                #if q1 == "loop":
                    #continue
                if (q1 == "Cannot Unify"):
                    continue
                res = resolve(q1)
                if res is True:
                    return True
                loop.clear()
                #print loop
    return False
            
inputFile = open("input.txt","r")
outputFile = open("output.txt","w")
#pdb.set_trace()
#loop = set()
nQ = int(inputFile.readline())
Queries = []
for i in range(nQ):
    q = str(inputFile.readline())
    q = q.replace("\n","")  
    q = q.replace("\r","")
    q = q.replace("/r","")
    Queries.append(q)
nS = int(inputFile.readline())
counter = 0
Kb = []
Kb_pred = {}
loop = set()
for i in range(nS):
    s = str(inputFile.readline())
    s = s.replace("\n","")
    s = s.replace("\r","")
    s1 = standardize(s,i)
    Kb.append(s1)
    sp = getPredicates(s1)
    for item in sp:
        if item in Kb_pred:
            Kb_pred[item].append(i)
        else:
            Kb_pred[item] = [i]
for q in Queries:
    start = time.time()
    #pdb.set_trace()
    print q
    try:
        if q[0] == "~":
            q2 = q[1:]
        else:
            q2 = "~" + q
        first_string = q2
        Kb.append(q2)
        pred = getPredicates(q)
        for p in pred:
            if p[0] == "~":
                p2 = p[1:]
            else:
                p2 = "~" + p
            if p2 in Kb_pred:
                Kb_pred[p2].append(nS)
            else:
                Kb_pred[p2] = [nS]
            index = findPredicate(p)
            if (index < 0) or len(index) is 0:
                outputFile.write("FALSE"+"\n")
                #print "in here"
                #print "false"
                del Kb[-1]
                del Kb_pred[p2][-1]
                loop.clear()
            
            else:
                for i in index:
                    q1 = unify(q2,Kb[i],p)
                    res = resolve(q1)
                    if res is True:
                        outputFile.write(str(res).upper()+"\n")
                        del Kb[-1]
                        del Kb_pred[p2][-1]
                        loop.clear()
                        #print loop
                        break
                    else:
                        pass
                if res is False:
                    outputFile.write(str(res).upper()+"\n")
                    del Kb[-1]
                    del Kb_pred[p2][-1]
                    loop.clear()
                    #print loop
    except RuntimeError:
        outputFile.write("FALSE"+"\n")    
        del Kb[-1]
        del Kb_pred[p2][-1]   
        loop.clear()
        #print loop