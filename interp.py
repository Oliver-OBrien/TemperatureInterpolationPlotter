#This file is contains all of the interpolation functions used in the project.
#
#It also contains a linear approximation function which is not used. That 
#function was intendid to be used with to find the best points to pass to the
#Lagrange polynomial method, but there were still too many points unless psi
#was particularly high, at which point comparison to the other algorithms
#would not make much sense. This is demonstrated in old_main.py.

import math
import numpy as np

#linear interpolation
def linear(xs, ys, axs):
    xi = 0
    ai = 0
    eys = []
    while xi < len(xs):
        if axs[ai] == xs[xi]:
            eys.append(ys[xi])
            ai += 1
            xi += 1
        else:
            m = (ys[xi]-ys[xi-1]) / (xs[xi]-xs[xi-1])
            b = ys[xi]
            x = axs[ai]-xs[xi]
            eys.append(m*x+b)
            ai += 1
    while len(eys) < len(axs):
        eys.append(ys[xi-1])
    return eys

#Lagrange polynomial interpolation
def lagrange(xs, ys, axs):
    ai = 0
    xi = 0
    eys = []
    while xi < len(xs):
        if axs[ai] == xs[xi]:
            eys.append(ys[xi])
            ai += 1
            xi += 1
        else:
            #find the polynomial
            ey = 0
            for i in range(len(xs)):
                L = 1
                for j in range(len(xs)):
                    if i != j:
                        L *= (axs[ai]-xs[j]) / (xs[i]-xs[j])
                ey += L*ys[i]
            eys.append(ey)
            ai += 1
    while len(eys) < len(axs):
        eys.append(ys[xi-1])
    return eys

#piecewise linear approximation
def best_points(xs, ys, psi):
    nxs = [xs[0]]
    nys = [ys[0]]
    ls = 0 #line start
    su = 0 #slope upper limit
    sl = 0 #slope lower limit
    for i in range(1,len(xs)-1):
        if not ls == i-1:
            tsu = (ys[i]-nys[-1]+psi) / (xs[i]-nxs[-1])
            tsl = (ys[i]-nys[-1]-psi) / (xs[i]-nxs[-1])
            #check if valid line before next part
            if tsu < sl or tsl > su:
                #add point at previous x
                ny = (xs[i-1]-nxs[-1])*(su+sl)/2+nys[-1]
                nxs.append(xs[i-1])
                nys.append(ny)
                ls = i-1
            else:
                if tsu < su: su = tsu
                if tsl > sl: sl = tsl
        if ls == i-1:
            su = (ys[i]-nys[-1]+psi) / (xs[i]-nxs[-1])
            sl = (ys[i]-nys[-1]-psi) / (xs[i]-nxs[-1])
    ny = (xs[i-1]-nxs[-1])*(su+sl)/2+nys[-1]
    nxs.append(xs[i-1])
    nys.append(ny)
    return [nxs, nys]

#cubic spline
def cubic_spline(xs, ys, axs):
    A = []
    a = [1.]
    h = []
    #populate A
    #first row and h
    for i in range(1,len(xs)):
        a.append(0.)
        h.append(xs[i]-xs[i-1])
    A.append(np.array(a))
    #middle rows
    for i in range(1,len(xs)-1):
        a = []
        #add leading zeros
        for j in range(0,i-1):
            a.append(0.)
        #add non-zero elements
        a.append(h[i-1])
        a.append(2*(h[i-1]+h[i]))
        a.append(h[i])
        #add trailing zeros
        for j in range(i+1,len(xs)-1):
            a.append(0.)
        #add row to A
        A.append(np.array(a))
    a = []
    #last row
    for i in range(0,len(xs)-1):
        a.append(0.)
    a.append(1.)
    A.append(np.array(a))
    #populate b
    b = [0.]
    for i in range(1,len(xs)-1):
        b.append(3./h[i]*(ys[i+1]-ys[i]) - 3./h[i-1]*(ys[i]-ys[i-1]))
    b.append(0.)
    #find c, from Ac=b
    c = np.linalg.solve(np.array(A),np.array(b))
    #find b and d
    b = []
    d = []
    for i in range(0,len(xs)-1):
        b.append(1/h[i]*(ys[i+1]-ys[i]) - h[i]/3*(2*c[i]+c[i+1]))
        d.append(1/(3*h[i])*(c[i+1]-c[i]))
    #apply spline
    ai = 0
    xi = 0
    eys = []
    while xi < len(xs):
        if axs[ai] == xs[xi]:
            eys.append(ys[xi])
            ai += 1
            xi += 1
        else:
            #y = that equation
            x = axs[ai] - xs[xi-1] #seems like this should be xi-1
            i = xi-1
            ey = ys[i] + b[i]*x + c[i]*x**2 + d[i]*x**3
            eys.append(ey)
            ai += 1
    while len(eys) < len(axs):
        eys.append(ys[xi-1])
    return eys
 
#error calculations
def average_error(xs, ys, eys):
    tot_err = 0
    for i in range(len(xs)):
        tot_err += abs(ys[i] - eys[i])
    avg_err = tot_err / len(xs)
    return avg_err

def rms_error(xs, ys, eys):
    tot_squ = 0
    for i in range(len(xs)):
        tot_squ += math.pow(ys[i] - eys[i], 2)
    rms_err = math.sqrt(tot_squ / len(xs))
    return rms_err
