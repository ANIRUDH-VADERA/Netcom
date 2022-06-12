ip=input("Input the IPv4 Address which you want to validate : ") 
l=ip.split('.') 
temp=l[-1].split('/') 
l[-1]=temp[0] 
l.append(temp[1]) 
b=[] 
for i in range(len(l)): 
    l[i]=int(l[i]) 
for i in range(len(l)-1):     
    if l[i]>=0 and l[i]<=255: 
        b.append(bin(l[i])[2:])     
    else:         
        print("No")         
        exit() 
for i in range(len(l)-1):     
    while len(b[i])<8:         
        b[i]='0'+b[i] 
cl='' 
if b[0]=='0':     
    cl="A" 
elif b[0][0:2]=="10": 
    cl="B" 
elif b[0][0:3]=="110": 
    cl="C"
elif b[0][0:4]=="1110": 
    cl="D"
elif b[0][0:4]=="1111": 
    cl="E" 
if cl=="A":     
    nbdm=8 
elif cl=="B":     
    nbdm=16 
elif cl=="C":     
    nbdm=24 
nsubnets=2**(l[-1]-nbdm) 
nhs=(2**(32-l[-1]))-2 
z=32-l[-1] 
c=0 
for i in range(len(l)-2, -1, -1):     
    if z>=8:         
        b[i]="00000000"         
        z-=8     
    else: 
        b[i]=b[i][:8-z]         
        while z>0:             
            b[i]+='0' 
            z-=1 
sa=[] 
for i in range(len(b)):     
    sa.append(int(b[i], 2)) 
temp="" 
for i in range(len(sa)):     
    temp+=str(sa[i])     
    if i!=len(sa)-1:         
        temp+="." 
temp1="" 
temp2="" 
for i in range(len(sa)):     
    if i == len(sa)-1:         
        temp1+=str(sa[i]+1)         
        temp2+=str(sa[i]+nhs+1)     
    else: 
        temp1+=str(sa[i])         
        temp2+=str(sa[i])     
    if i!=len(sa)-1:         
        temp1+='.'         
        temp2+='.' 
broad_Id = temp2
temp2 = temp2[0:-1] + str(int(temp2[-1])-1)
print("(If this was a classlfull addressing)Class: ", cl) 
print("1. Number of Subnets: ", nsubnets) 
print("2. Subnet address: ", temp) 
print("3. Broadcast Address: ", broad_Id) 
print("4. Number of hosts per subnet: ", nhs) 
print("5. First Host id: ", temp1) 
print("6. Last Host id: ", temp2) 
print("ANIRUDH VADERA(20BCE2940)")