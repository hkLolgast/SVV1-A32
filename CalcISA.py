import math, time
def meter(ft):
    return ft*0.3048

def ft(meter):
    return meter/0.3048
    
baseValues = {
#     "h"  : meter(5000.),
    "T"  : 288.15,
    "P"  : 101325.,
    "rho": 1.225
    }
    
constants = {
    "g0": 9.80665,
    "R" : 287.00,
     "a" : [-0.0065,
            0,
            0.001,
            0.0028,
            0,
            -0.0028,
            -0.002]
    }
    
layers = [0,
          11000,
          20000,
          32000,
          47000,
          51000,
          71000,
          84852]
    
def valuesAtHeight(h1):
    if h1==0:
        return baseValues["T"], baseValues["P"], baseValues["rho"]
    if h1<0 or h1>layers[-1]:
        raise ValueError, "Heights above %d or below 0 not supported" % layers[-1]
    g0  = constants["g0"]
    R   = constants["R"]
    layer = -1
    while h1>layers[layer+1]:
        layer+=1
    a = constants["a"][layer]
#     print h1, layer
    if layer==0:
        h0  = 0
        T0  = baseValues["T"]
        P0  = baseValues["P"]
        rho0= baseValues["rho"]
    else:
        h0 = layers[layer]
#         print "h1, h0:",h1, h0
        T0, P0, rho0 = valuesAtHeight(h0)
    if a!=0:
        T1   = T0+a*(h1-h0)
        P1   = P0*((T1/T0)**(-g0/(a*R)))
        rho1 = rho0*((T1/T0)**(-g0/(a*R)-1))
    else:
        T1   = T0
        P1   = P0*(math.exp(-g0/(R*T0)*(h1-h0)))
        rho1 = rho0*(math.exp(-g0/(R*T0)*(h1-h0)))
        
    return T1, P1, rho1

def calcHeight(P1):
    g0  = constants["g0"]
    R   = constants["R"]
#     a   = constants["a"]
#     h0  = baseValues["h"]
    T0  = baseValues["T"]
    P0  = baseValues["P"]
    rho0= baseValues["rho"]
    
    if P1<valuesAtHeight(11000)[1]:
        T0, P0, rho0 = valuesAtHeight(11000)
        h0=11000
        return(-R*T0*math.log(P1/P0)/g0+h0)
    else:
        a = constants["a"][0]
        return((T0/a)*((P1/P0)**(-a*R/g0)-1))

if __name__=="__main__":
    
    close = False
            
    while not close:
    
        print("What do you want to do?")
        print("\t1) Calculate P, T and rho (altitude in meter)")
        print("\t2) Calculate P, T and rho (altitude in feet)")
        print("\t3) Calculate altitude at given pressure")
        print("\t4) Exit")
        choice = raw_input("Your choice: ")
        if choice != "1" and choice != "2" and choice != "3" and choice != "4":
            print("Invalid choice. Choose from 1, 2 or 3")
            validChoice = False
        else:
            validChoice = True
    
        if validChoice:
            if choice=="1" or choice=="2":        
                h1 = raw_input("Enter altitude: ")
                validHeight = True
                try:
                    h1=float(h1)
                except:
                    validHeight = False
                    print("Invalid input: expected number, got "+str(type(h1)))
    
                if validHeight:
                    if choice=="2":
                        h1=meter(h1)
                    
                    try:
                        T1, P1, rho1 = valuesAtHeight(h1)
                    except ValueError:
                        print "Only heights 0<h<=84852 are supported"
                    else:
                        print("\nT: "+str(T1)+" [K]")
                        print("P: "+str(P1)+" [Pa]")
                        print("rho: "+str(rho1)+" [kg m^-3]\n")
                    
    
            elif choice=="3":
                P1 = raw_input("Enter pressure: ")
                validPressure = True
                try:
                    P1 = float(P1)
                except:
                    validPressure = False
                    print("Invalid input: expected number, got "+str(type(P1)))
                if validPressure:
                    h1=calcHeight(P1)
                    h1ft=ft(h1)
                    if h1>20000:
                        print("\nThis pressure results in an altitude above 20km. Calculation is not supported.\n")
                    elif h1<0:
                        print("\nThis pressure results in a negative altitude. Either you're trying to land on Schiphol or you crashed\n")
                    else:
                        print("\n"+str(h1)+" [m]")
                        print(str(h1ft)+" [ft]")
                        print("FL"+"0"*(3-len(str(int(h1ft/100))))+str(int(h1ft/100))+"\n")
                        #print("\n"+str(h1)+" [m]"+str(h1ft)+" ft, FL"+"0"*(3-len(str(int(h1ft/100))))+str(int(h1ft/100))+"\n")
            elif choice=="4":
                close = True
            else:
                print("Something somewhere went terribly wrong")
                close = True
                
    print("Goodbye!")        
    time.sleep(1)