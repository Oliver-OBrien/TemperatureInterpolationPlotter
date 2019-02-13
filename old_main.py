#This file was used to while to test interpolation functions on the data from
#January 1st, 2017. It includes more applications of those functions than
#find_results.py, but tests those applications much less thouroughly.

import matplotlib as mpl
mpl.use('svg') #this line allows figures to be created without an X-server
import matplotlib.pyplot as plt
from interp import *

#get data from file
xs = []
ys = []
file = open("data/tempc1.txt","r")
xstring = file.readline().strip().split(" ")
ystring = file.readline().strip().split(" ")
file.close()
for i in range(len(ystring)):
    minutes = 60*float(xstring[2*i+1][:-3])+float(xstring[2*i+1][3:])
    xs.append(minutes)
    ys.append(float(ystring[i]))

#plot data
plt.plot(xs, ys)
plt.savefig("images/tempc_true.png")
plt.clf()

#cut out 90% of the data and plot again
xs10 = []
ys10 = []
for i in range(len(xs)/10):
    xs10.append(xs[i*10])
    ys10.append(ys[i*10])
if len(xs)%10 != 0:
    xs10.append(xs[len(xs)-1])
    ys10.append(ys[len(xs)-1])
plt.plot(xs10, ys10)
plt.savefig("images/tempc_10-percent.png")
plt.clf()

#cut out 95% of the data and plot again
xs5 = []
ys5 = []
for i in range(len(xs)/20):
    xs5.append(xs[i*20])
    ys5.append(ys[i*20])
if len(xs)%20 != 0:
    xs5.append(xs[len(xs)-1])
    ys5.append(ys[len(xs)-1])
plt.plot(xs5, ys5)
plt.savefig("images/tempc_5-percent.png")
plt.clf()

#use interpolation methods to fill in points
#linear interpolation 10p
eys = linear(xs10, ys10, xs)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_linear_10p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("linear RMS error with 10%: "+str(rms_err))

#linear interpolation 5p
eys = linear(xs5, ys5, xs)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_linear_5p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("linear RMS error with 5%: "+str(rms_err))

#Lagrange polynomial interpolation with 10%
eys = lagrange(xs10, ys10, xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_lagrange_10p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("Lagrange RMS error with 10%: "+str(rms_err))

#Lagrange polynomial interpolation with 5%
eys = lagrange(xs5, ys5, xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_lagrange_5p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("Lagrange RMS error with 5%: "+str(rms_err))

#linear estimation with 100%
bps = best_points(xs, ys, .5)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(bps[0], bps[1])
plt.savefig("images/tempc_linear_est_100p.png")
plt.clf()
rms_err = rms_error(xs, ys, linear(bps[0],bps[1],xs))
print("linear estimation RMS error with 100%: "+str(rms_err)+" (with "+str(len(bps[0]))+" points)")

#Lagrange with linear estimation points
bps = best_points(xs, ys, .5)
eys = lagrange(bps[0], bps[1], xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_lag_linear_est.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("Lagrange with linear estimation RMS error: "+str(rms_err)+" (with "+str(len(bps[0]))+" points)")

#cubic spline interpolation with 5%
eys = cubic_spline(xs5, ys5, xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_cubic_5p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("cubic spline RMS error with 5%: "+str(rms_err))

#cubic spline interpolation with 10%
eys = cubic_spline(xs10, ys10, xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_cubic_10p.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("cubic spline RMS error with 10%: "+str(rms_err))

#cubic with linear estimation points
bps = best_points(xs, ys, .1)
eys = cubic_spline(bps[0], bps[1], xs)
fig, ax = plt.subplots()
ax.set_ylim(-10,3)
plt.plot(xs, ys)
plt.plot(xs, eys)
plt.savefig("images/tempc_cubic_linear_est.png")
plt.clf()
rms_err = rms_error(xs, ys, eys)
print("cubic spline with linear estimation RMS error: "+str(rms_err)+" (with "+str(len(bps[0]))+" points)")
