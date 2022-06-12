import math

def calhost(rec,cal):
    h="0.0.0.0"
    host = h.split(".")
    for i in range(4):
        if cal[i]=="255":
            host[i]=rec[i]
        elif cal[i]=="0":
            host[i]=cal[i]
        else:
            host[i]=str(int(rec[i])&int(host[i]))
    return(host)


def main():    
    ip = input("Enter an IPv4 Address\n")
    classless = "/"
    if classless not in ip:
        print("Addressing style used is Classful\n")
        rec = ip.split(".")
        id = int(rec[0])
        if id<128:
            print("Address belongs to class A\n")
            mask = "255.0.0.0"
            cal = mask.split(".")
            host = calhost(rec,cal)
            print("Default mask for class A is: {}\n".format(mask))
            print("Host address: {}.{}.{}.{}\n".format(host[0],host[1],host[2],host[3]))
            non=math.pow(2,7)
            noh=math.pow(2,24)
            print("Number of networks: {} and number of hosts: {}\n".format(non,noh))
            print("Network Address of {} is {}.{}.{}.{} and Direct Broadcast Address is: {}.{}.{}.{}\n".format(ip,rec[0],"0","0","0",rec[0],"255","255","255"))
        elif id<192:
            print("Address belongs to class B\n")
            mask = "255.255.0.0"
            cal = mask.split(".")
            host = calhost(rec,cal)
            print("Default mask for class B is: {}\n".format(mask))
            print("Host address: {}.{}.{}.{}\n".format(host[0],host[1],host[2],host[3]))
            non=math.pow(2,14)
            noh=math.pow(2,16)
            print("Number of networks: {} and number of hosts: {}\n".format(non,noh))
            print("Network Address of {} is {}.{}.{}.{} and Direct Broadcast Address is: {}.{}.{}.{}\n".format(ip,rec[0],rec[1],"0","0",rec[0],rec[1],"255","255"))
        elif id<224:
            print("Address belongs to class C\n")
            mask = "255.255.255.0"
            cal = mask.split(".")
            host = calhost(rec,cal)
            print("Default mask for class C is: {}\n".format(mask))
            print("Host address: {}.{}.{}.{}\n".format(host[0],host[1],host[2],host[3]))
            non=math.pow(2,21)
            noh=math.pow(2,8)
            print("Number of networks: {} and number of hosts: {}\n".format(non,noh))
            print("Network Address of {} is {}.{}.{}.{} and Direct Broadcast Address is: {}.{}.{}.{}\n".format(ip,rec[0],rec[1],rec[2],"0",rec[0],rec[1],rec[2],"255"))
        elif id<240:
            print("Address belongs to class D\n")
        elif id<256:
            print("Address belongs to class E\n")
    elif classless in ip:
        print("Addressing style used is Classful\n")
        x=ip.split("/")
        rec=x[0].split(".")
        mv=int(x[1])
        nos= mv/8
        rem = mv%8
        cal=[]
        for i in range(4):
            if i<nos:
                cal.append("255")
            elif i == nos:
                sum=0
                while(rem>0):
                        sum = sum + math.pow(2,7-rem)
                        rem = rem - 1
                cal.append(str(sum))
            else:
                cal.append("0")
        host = calhost(rec,cal)
        print("Mask is: {}.{}.{}.{}\n".format(cal[0],cal[1],cal[2],cal[3]))
        print("Host address: {}.{}.{}.{}\n".format(host[0],host[1],host[2],host[3]))
        id = int(rec[0])
        if id<128:
            print("Address belongs to class A\n")
            nor=8
        elif id<192:
            print("Address belongs to class B\n")
            nor=16;
        elif id<224:
            print("Address belongs to class C\n")
            nor=24;
        elif id<240:
            print("Address belongs to class D\n")
        elif id<256:
            print("Address belongs to class E\n")   
        nos=math.pow(2,(mv-nor))
        noh=math.pow(2,(32-mv))-2
        print("Number of subnets: {} and number of hosts per subnet: {}\n".format(nos,noh))

if __name__ == "__main__":
    print("ANIRUDH VADERA(20BCE2940)")
    main()