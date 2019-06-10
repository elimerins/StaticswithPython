import numpy as np
import math
from math import exp
from scipy.integrate import quad
from scipy import stats
from decimal import Decimal
import operator as op
from functools import reduce

def ncr(n, r):
    numer=1
    denom=1
    for i in range(1,int(r)+1):
        denom*=i
        numer*=n+1-i
    return Decimal(numer/denom)
#Combination 계산 함수
print(stats.norm.ppf(1-0.1/2))
print(stats.norm.ppf(1-0.05/2))
print(stats.norm.ppf(1-0.01/2))

testarr=[[9,1],
         [5,5]]


def cmh_test(testarr,alpha):
    testnp = np.array(testarr)
    n = np.sum(testnp[:, :])
    allColumns = len(testarr[0])
    allRows = len(testarr)
    Zalpha2=stats.norm.ppf(1 - alpha/2)
    print(Zalpha2)
    matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
    U = [[0 for col in range(allColumns)] for row in range(allRows)]
    V = [[0 for col in range(allColumns)] for row in range(allRows)]
    for i in range(allRows):
        for j in range(allColumns):
            U[i][j] = allRows - i
            print("i j : " + str(i) + str(j))
            print(U[i][j])
            V[i][j] = allColumns - j
            print(V[i][j])

    Ubar = 0
    Vbar = 0
    for i in range(allRows):
        Ubar += U[i][0] * np.sum(testnp[i, :]) / n
    for i in range(allColumns):
        Vbar += V[0][i] * np.sum(testnp[:, i]) / n
    print(Ubar, Vbar)

    sumPihatij = 0
    sumPihatit = 0
    sumPihattj = 0
    for i in range(allRows):
        for j in range(allColumns):
            sumPihatij += (U[i][j] - Ubar) * (V[i][j] - Vbar) * testnp[i, j] / n
    for i in range(allRows):
        sumPihatit += math.pow((U[i][0] - Ubar), 2) * np.sum(testnp[i, :]) / n
    for i in range(allColumns):
        sumPihattj += math.pow(V[0][i] - Vbar, 2) * (np.sum(testnp[:, i]) / n)

    print(sumPihatij)
    print(sumPihatit)
    print(sumPihattj)
    phat = sumPihatij / math.pow(sumPihatit * sumPihattj, 0.5)
    print(phat)
    print(phat ** 2)
    Msquare = (n - 1) * (phat ** 2)
    print(Msquare ** 0.5)
    return round(Msquare**0.5,4),round(phat,4),round(Zalpha2,4)

def Residuals(testarr):
    testnp=np.array(testarr)
    n=np.sum(testnp[:, :])
    allColumns=len(testarr[0])
    allRows=len(testarr)
    matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
    pm_matrix = [[0 for col in range(allColumns)] for row in range(allRows)]
    #+,-기호를 저장할 matrix

    for i in range(len(testarr)):
        for j in range(len(testarr[0])):
            Nit=np.sum(testnp[i,:],axis=0)
            Ntj=np.sum(testnp[:,j],axis=0)
            Mij = Nit * Ntj / n
            rij=(testnp[i,j]-Mij)/math.pow(Mij*(1-Nit/n)*(1-Ntj/n),0.5)
            print("Rij")

            if rij>=2.5758293035489004:
                pm_matrix[i][j]="+++"
            elif 1.959963984540054<=rij and rij<2.5758293035489004:
                pm_matrix[i][j]="++"
            elif 1.6448536269514722<=rij and rij<1.959963984540054:
                pm_matrix[i][j]="+"
            elif rij<=-2.5758293035489004:
                pm_matrix[i][j]="---"
            elif -1.959963984540054>=rij and rij > -2.5758293035489004:
                pm_matrix[i][j]="--"
            elif -1.6448536269514722>=rij and rij > -1.959963984540054:
                pm_matrix[i][j]="-"
            matrix[i][j]=round(rij,4)
    return matrix,pm_matrix
def greater_less(testarr):
    odds, pvalue = stats.fisher_exact(testarr)
    odds,lpvalue=stats.fisher_exact(testarr,'less')
    print(odds,lpvalue)
    odds, gpvalue = stats.fisher_exact(testarr, 'greater')
    print(odds, gpvalue)

    return gpvalue,lpvalue,pvalue

def Cal_D_value(testarr,alpha):
    testnp = np.array(testarr)
    n = np.sum(testnp[:, :])
    print(n)  # sum of all elements in matrix
    N1t = np.sum(testnp[0, :], axis=0)
    N2t = np.sum(testnp[1, :], axis=0)
    Nt1 = np.sum(testnp[:, 0], axis=0)
    Nt2 = np.sum(testnp[:, 1], axis=0)
    pi1 = testnp[0, 0] / N1t
    pi2 = testnp[1, 0] / N2t
    SE = math.pow(pi1 * (1 - pi1) / N1t + pi2 * (1 - pi2) / N2t, 0.5)
    print("SE : " + str(SE))
    Zalpha2 = stats.norm.ppf(1 - alpha / 2)
    plus = (pi1 - pi2) + Zalpha2 * SE
    minus = (pi1 - pi2) - Zalpha2 * SE
    if plus*minus<=0:
        text="The proportions are equal"
    else:
        text = "The proportions are not equal"
    print(plus)
    print(minus)
    #testnp[0, 0] / np.sum(testnp[0, :], axis=0) - testnp[1, 0] / np.sum(testnp[1, :], axis=0)
    return pi1,pi2,plus,minus,text

def Cal_OR_value(testarr,alpha):
    testnp = np.array(testarr)
    if np.min(testnp)<=0:
        Message="minimum value in matrix is less than 0\n all of matrix value are higher than 0"
        return Message,0,0,0,0
    n = np.sum(testnp[:, :])
    print(n)  # sum of all elements in matrix
    OR=testnp[0,0]*testnp[1,1]/testnp[1,0]*testnp[0,1]
    print(OR)
    N1t = np.sum(testnp[0, :], axis=0)
    N2t = np.sum(testnp[1, :], axis=0)
    Nt1 = np.sum(testnp[:, 0], axis=0)
    Nt2 = np.sum(testnp[:, 1], axis=0)
    pi1 = testnp[0, 0] / N1t
    pi2 = testnp[1, 0] / N2t
    SE = math.pow(1/testnp[0,0]+1/testnp[0,1]+1/testnp[1,0]+1/testnp[1,1],0.5)
    print("SE : " + str(SE))
    Zalpha2 = stats.norm.ppf(1 - alpha / 2)
    log_plus = math.log(OR) + Zalpha2 * SE
    log_minus = math.log(OR) - Zalpha2 * SE
    plus=exp(log_plus)
    minus = exp(log_minus)
    print(plus)
    print(minus)
    return OR,log_minus,log_plus,minus,plus

def Cal_RR_value(testarr,alpha):
    testnp = np.array(testarr)
    n = np.sum(testnp[:, :])
    print(n)  # sum of all elements in matrix
    pi1=testnp[0, 0] / np.sum(testnp[0, :], axis=0)
    pi2 = testnp[1, 0] / np.sum(testnp[1, :], axis=0)
    RR=pi1/pi2
    N1t = np.sum(testnp[0, :], axis=0)
    N2t = np.sum(testnp[1, :], axis=0)
    print((testnp[1,0]/np.sum(testnp[1, :], axis=0)))
    SE = math.pow((1-pi1)/(N1t*pi1)+(1-pi2)/(N2t*pi2),0.5)
    print(SE)
    Zalpha2 = stats.norm.ppf(1 - alpha / 2)
    log_plus = math.log(RR) + Zalpha2 * SE
    print(log_plus)
    log_minus=math.log(RR)-Zalpha2*SE
    plus = exp(log_plus)
    minus = exp(log_minus)
    print(plus)
    print(minus)
    return RR,log_minus,log_plus,minus,plus

def Cal_x_value(testarr):
    testnp=np.array(testarr,dtype=float)
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
    return round(ksquare,4),round(F,4)

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
    def f(Symbolx) :
        return 1/(math.gamma(r/2)*(2**(r/2)))*(Symbolx**((r/2)-1))*exp(-Symbolx/2)

    F,err= quad( f, sum, np.inf )
    print("p_value : "+str(F))
    return round(sum,4),round(F,4)
