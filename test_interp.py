#This file was used for debuging on a smaller dataset, so that intermediary
#values could be checked by hand.

import matplotlib as mpl
mpl.use('svg')
import matplotlib.pyplot as plt
from interp import *


#get data from file
xs = []
ys = []
file = open("data/triangle.txt","r")
xstring = file.readline().strip().split(" ")
ystring = file.readline().strip().split(" ")
file.close()
for i in range(len(ystring)):
    minutes = float(xstring[i])
    xs.append(minutes)
    ys.append(float(ystring[i]))

#interp
allxs = []
for i in range(10*len(xs)):
    allxs.append(i*.1)
estys = cubic_spline(xs, ys, allxs)
#while len(allxs) < len(estys):
#    estys = estys[:-1]
#while len(allxs) > len(estys):
#    allxs = allxs[:-1]

#plot data
plt.plot(xs, ys)
plt.plot(allxs, estys)
plt.savefig("tempc_interp_test.png")
#plt.show()
#plt.clf()
