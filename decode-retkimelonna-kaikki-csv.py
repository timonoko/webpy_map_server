import os

f=open("kaikki.csv","r")

def k(s1):
    s="".join(s1)
    s2=s.decode('iso-8859-1').encode('utf-8')
    return s2.strip("\n").replace('"',"")

print "["
eka=True
for line  in f:
    if not eka:
        print ","
    v=line.split(",")
#    print  "[",float(v[1]),", ",float(v[0]),", ",k(v[2:]),"]"
    print  '[%f,%f,"%s"]'%(float(v[1]),float(v[0]),k(v[2:])),
    eka=False
f.close()
print "]\n"



    

    
