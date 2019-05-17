import numpy as np
import math
from math import exp
from scipy.integrate import quad
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

testarr=[[9,1],
         [5,5]]

testnp = np.array(testarr)
r = (np.size(testnp, 1) - 1) * (np.size(testnp, 0) - 1)

n = np.sum(testnp[:, :])
print(n)  # sum of all elements in matrix
sum = 0
N1t = np.sum(testnp[0, :], axis=0)
N2t = np.sum(testnp[1, :], axis=0)
Nt1 = np.sum(testnp[:, 0], axis=0)
Nt2 = np.sum(testnp[:, 1], axis=0)
a=ncr(N1t,testnp[0, 0])
print(a)
b=ncr(N2t,Nt1-testnp[0, 0])
print(b)
c=ncr(n,Nt1)
print(c)
print(a*b/c)

def Cal_x_value(testarr):
    testnp=np.array(testarr)
    r=(np.size(testnp,1)-1)*(np.size(testnp,0)-1)

    n=np.sum(testnp[:,:])
    print(n)#sum of all elements in matrix
    sum=0
    for i in range(len(testarr)):
        for j in range(len(testarr[0])):
            Nit=np.sum(testnp[i,:],axis=0)
            print("Nit : "+str(Nit))
            Ntj=np.sum(testnp[:,j],axis=0)
            print("Ntj : "+str(Ntj))
            Mij=Nit*Ntj/n
            print("Mij : "+str(testnp[i,j]))
            print("testarr[I,J] : "+str(testnp[i,j]))
            element=pow(testnp[i,j]-Mij,2)/Mij
            print(element)
            sum=sum+element
            print("sum : "+str(sum))

    ksquare=(1/math.gamma(r/2)*pow(2,r))*pow(sum,r-1)*exp(-sum/2)
    print("Ksquare(X^2) : "+str(ksquare))
    """
    r=10
    sum=15.99
    """
    def f(Symbolx) :
        return 1/(math.gamma(r/2)*(2**(r/2)))*(Symbolx**((r/2)-1))*exp(-Symbolx/2)

    F,err= quad( f, sum, np.inf )
    print("p_value : "+str(F))
    return round(F,4)

def Cal_g_value(testarr):
    testnp=np.array(testarr)
    r=(np.size(testnp,1)-1)*(np.size(testnp,0)-1)

    n=np.sum(testnp[:,:])
    print(n)#sum of all elements in matrix
    sum=0
    for i in range(len(testarr)):
        for j in range(len(testarr[0])):
            Nit=np.sum(testnp[i,:],axis=0)
            print("Nit : "+str(Nit))
            Ntj=np.sum(testnp[:,j],axis=0)
            print("Ntj : "+str(Ntj))
            Mij=Nit*Ntj/n
            print("Mij : "+str(testnp[i,j]))
            print("testarr[I,J] : "+str(testnp[i,j]))
            element=testnp[i,j]*math.log(testnp[i,j]/Mij)
            print(element)
            sum=sum+element
            print("sum : "+str(sum))
    sum=2*sum
    print("g^2 : "+str(sum))
    #ksquare=(1/math.gamma(r/2)*pow(2,r))*pow(sum,r-1)*exp(-sum/2)
    #print("Ksquare(X^2) : "+str(ksquare))
    """
    r=10
    sum=15.99
    """
    def f(Symbolx) :
        return 1/(math.gamma(r/2)*(2**(r/2)))*(Symbolx**((r/2)-1))*exp(-Symbolx/2)

    F,err= quad( f, sum, np.inf )
    print("p_value : "+str(F))
    return round(F,4)
def Cal_g_value(testarr):
    testnp=np.array(testarr)
    r=(np.size(testnp,1)-1)*(np.size(testnp,0)-1)

    n=np.sum(testnp[:,:])
    print(n)#sum of all elements in matrix
    sum=0
    N1t = np.sum(testnp[0, :], axis=0)
    N2t = np.sum(testnp[1, :], axis=0)
    Nt1 = np.sum(testnp[:, 0], axis=0)
    Nt2 = np.sum(testnp[:, 1], axis=0)

    print(len(combinations(N1t,int(testnp[0,0])))*len(combinations(N2t,Nt1-int(testnp[0,0])))/len(combinations(n,Nt1)))
    """
    for i in range(len(testarr)):
        for j in range(len(testarr[0])):
            Nit=np.sum(testnp[i,:],axis=0)
            print("Nit : "+str(Nit))
            Ntj=np.sum(testnp[:,j],axis=0)
            print("Ntj : "+str(Ntj))
            Mij=Nit*Ntj/n
            print("Mij : "+str(testnp[i,j]))
            print("testarr[I,J] : "+str(testnp[i,j]))
            element=testnp[i,j]*math.log(testnp[i,j]/Mij)
            print(element)
            sum=sum+element
            print("sum : "+str(sum))
    sum=2*sum
    
    print("g^2 : "+str(sum))
    #ksquare=(1/math.gamma(r/2)*pow(2,r))*pow(sum,r-1)*exp(-sum/2)
    #print("Ksquare(X^2) : "+str(ksquare))
    
    
    def f(Symbolx) :
        return 1/(math.gamma(r/2)*(2**(r/2)))*(Symbolx**((r/2)-1))*exp(-Symbolx/2)

    F,err= quad( f, sum, np.inf )
    print("p_value : "+str(F))
    """

    #return round(F,4)
#print(round(F, 4))
#print(np.size(testnp,1))#counts of columns
