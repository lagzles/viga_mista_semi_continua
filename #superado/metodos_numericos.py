import math

def integral_primeira(f, xi, xf):
##    n = 1000 # numero de divisoes precisa ser PAR
    a = xi
    b = xf
    h = 0.05  # (b-a) / n

    n = math.ceil((b-a) / h)
    if n % 2 != 0:
        n += 1

    s = 0

    for i in range(1, n):
        
        s += f(a+i*h)*h

    integrall = 1 * s
    
    return integrall


def integral_segunda(f, xi, xf):
##    n = 1000 # numero de divisoes precisa ser PAR
    a = xi
    b = xf
    h = 0.05  # (b-a) / n

    n = math.ceil((b-a) / h)
    if n % 2 != 0:
        n += 1

    s = 0
    lista_integral_primeira = []
    
    for i in range(1, n):
##        s += f(a+i*h)*h
        s = integral_primeira(f,a, a+i*h)
        lista_integral_primeira.append(s)
        
    s = 0
    for i in lista_integral_primeira:
        s += i*h
    integrall = 1 * s
    
    return integrall


def integral_um(xp, ypm, xf):    
    integ = 0
    step = 0.1
    for j in range(len(xp)):
        if xp[j] <= xf:
            integ += ypm[j]  * step
##        else:
##            print(xf)
##            return integ
    return integ

def integral_dois(xp, ypm, xf):
    integ2 = 0
    step = 0.1
    for k in range(len(xp)):
        if xp[k] <= xf:
            for j in range(len(xp)):
                if xp[j] <= xp[k]:
                    integ2 += ypm[j] * step
##                else:
####                    print('else 1 ',xp[j], xf)
##                    break
##        else:
####            print('else 2 ',xp[k], xf)
##            break
    return integ2


def get_root(f, fl, x):
##    x = 1
    if fl(x) == 0.0:
        xnew = x
        return xnew
    
    for i in range(1,101):
        xnew = x - f(x) / fl(x)
##        if xnew == nan:
##            xnew = 0.0
##            break
        if abs(xnew - x) < 0.0001:
            break
    
    
    return xnew    


