#this is the file that was used to find the values used in the summary. It
#uses each method on data from the first day of each month of 2017 prints some
#information about RMS error values for each one. Additionally, it saves images
#of graphs of the results of each method in the images folder. These images are
#named in the following way: tempc[month number]_[method].png

import matplotlib as mpl
mpl.use('svg') #this line allows figures to be created without an X-server
import matplotlib.pyplot as plt
from interp import *

#initialize err
err = []

#go through each dataset and compare methods
for t in range(1,13):
    #add err dict for current month
    err.append({})
    #get data from file
    xs = []
    ys = []
    file = open("data/tempc"+str(t)+".txt","r")
    xstring = file.readline().strip().split(" ")
    ystring = file.readline().strip().split(" ")
    file.close()
    for i in range(len(ystring)):
        minutes = 60*float(xstring[2*i+1][:-3])+float(xstring[2*i+1][3:])
        xs.append(minutes)
        ys.append(float(ystring[i]))
    #find ymax and ymin
    ymax = ys[0]
    ymin = ys[0]
    for y in ys:
        if y > ymax:
            ymax = y
        if y < ymin:
            ymin = y
    #plot data
    fig, ax = plt.subplots()
    ax.set_ylim(ymin-.5,ymax+.5)
    plt.ylabel("temperature (C)")
    plt.xlabel("time (minutes)")
    plt.plot(xs, ys)
    plt.savefig("images/tempc"+str(t)+"_full.png")
    plt.close(fig)
    #cut out 90% of the data and plot again
    xs10 = []
    ys10 = []
    for i in range(len(xs)/10):
        xs10.append(xs[i*10])
        ys10.append(ys[i*10])
    if len(xs)%10 != 0:
        xs10.append(xs[len(xs)-1])
        ys10.append(ys[len(xs)-1])
    fig, ax = plt.subplots()
    ax.set_ylim(ymin-.5,ymax+.5)
    plt.ylabel("temperature (C)")
    plt.xlabel("time (minutes)")
    plt.plot(xs10, ys10)
    plt.savefig("images/tempc"+str(t)+"_10-percent.png")
    plt.close(fig)
    #linear interpolation
    fig, ax = plt.subplots()
    ax.set_ylim(ymin-.5,ymax+.5)
    eys = linear(xs10, ys10, xs)
    plt.ylabel("temperature (C)")
    plt.xlabel("time (minutes)")
    plt.plot(xs, ys)
    plt.plot(xs, eys)
    plt.savefig("images/tempc"+str(t)+"_linear.png")
    plt.close(fig)
    rms_err = rms_error(xs, ys, eys)
    err[t-1]['linear'] = rms_err
    #Lagrange polynomial interpolation
    eys = lagrange(xs10, ys10, xs)
    fig, ax = plt.subplots()
    ax.set_ylim(ymin-.5,ymax+.5)
    plt.ylabel("temperature (C)")
    plt.xlabel("time (minutes)")
    plt.plot(xs, ys)
    plt.plot(xs, eys)
    plt.savefig("images/tempc"+str(t)+"_lagrange.png")
    plt.close(fig)
    rms_err = rms_error(xs, ys, eys)
    err[t-1]['Lagrange'] = rms_err
    #cubic spline interpolation
    eys = cubic_spline(xs10, ys10, xs)
    fig, ax = plt.subplots()
    ax.set_ylim(ymin-.5,ymax+.5)
    plt.ylabel("temperature (C)")
    plt.xlabel("time (minutes)")
    plt.plot(xs, ys)
    plt.plot(xs, eys)
    plt.savefig("images/tempc"+str(t)+"_cubic.png")
    plt.close(fig)
    rms_err = rms_error(xs, ys, eys)
    err[t-1]['cubic spline'] = rms_err

#calculate average, maximum RMS error for each
average_err = err[0].copy()
max_err = err[0].copy()
print("full RMS error data:")
print("1: "+str(err[0]))
for i in range(1,len(err)):
    print(str(i+1)+": "+str(err[i]))
    for k in err[i]:
        average_err[k] += err[i][k]
        if err[i][k] > max_err[k]:
            max_err[k] = err[i][k]
for k in average_err:
    average_err[k] = average_err[k] / len(err)
    print("average RMS error for "+k+": "+str(average_err[k]))
    print("maximum RMS error for "+k+": "+str(max_err[k]))

