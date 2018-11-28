'''
Created on 11.09.2018

@author: christian
'''
from qao.io import ionfile
import numpy as np
import pylab as p
import os, glob, sys
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as cm
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, fmin
from scipy import asarray as ar, exp
import xlwt, xlrd
from ionImage_datawriter import data_output
from ionImage_datawriter_wiki import data_output_2
import pprint

# from colorMap_wjet import wjet
cl = [(1, 1, 1), (1, 0, 0), (1, 0.9, 0)]
test = cm.LinearSegmentedColormap.from_list("bla", cl)

########################################################################
# Parameter
########################################################################
path_qao = "/media/Group"
patternPath = os.path.join(path_qao, "Group1/Lab/miscellaneous/pattern")
measurementDirectories = glob.glob('/home/johannes/Current_Data/gausskasten_feinmessung_2_2/minus31000/*/')
savePath = "/home/johannes/Current_Data/SEM_Data_2018_10_17&18/minus31000_Auswertung/"

saveResults = True
showPlots = True

scanName = "picture"

# default values for binning
yBin = 100
xBin = 100

########################################################################
# Calculations
########################################################################
for measurementDirectory in measurementDirectories:
    outName = measurementDirectory.split("/")[-3] + '_' + measurementDirectory.split("/")[-2]
    print(outName)
    # initialize IonMeasurement class
    im = ionfile.IonMeasurement(measurementDirectory, patternPath=patternPath)

    # special case: if we have a "normal" scan pattern extract
    # line number to set best binning for the image
    # if im.getScanDescriptor(scanName).parameterName == "lines":
    #     yBin = im.getScanDescriptor(scanName).parameterValue
    #     xBin = im.getScanDescriptor(scanName).samplerate * im.getScanDescriptor(scanName).duration / float(yBin)

    # get image from files
    data, xedges, yedges = im.getImage(scanName, [yBin, int(xBin)])

    # plot result
    sr = im.getScanDescriptor(scanName).scanRegion
    extent = [0, sr.width(), 0, sr.height()]

    fig = p.figure(figsize=(2, 8))
    ax = fig.add_subplot(111)
    p.suptitle(outName)
    p.xticks([])
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(0, np.shape(data)[1])
    ax.set_ylim(0, np.shape(data)[0])
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    im = ax.imshow(data, extent=extent, interpolation="nearest")
    # im = ax.imshow(data, cmap=wjet(), extent=extent, interpolation="nearest")

    divider = make_axes_locatable(ax)
    # integralPloty = divider.append_axes("top", size="20%", pad=0., sharex=ax)
    # summe = np.sum(data, axis=0)
    # # summe_y = np.linspace(0,len(summe),len(summe))
    # summe_y = np.linspace(extent[0], extent[1], len(summe))
    # integralPloty.clear()
    # integralPloty.get_xaxis().set_visible(False)
    # integralPloty.get_yaxis().set_visible(False)
    # # integralPloty.set_xlim(0,np.shape(data)[0])
    # # integralPloty.set_ylim(0,np.shape(data)[0])
    # integralPloty.plot(summe_y, summe)

    integralPlotx = divider.append_axes("right", size="40%", pad=0., sharey=ax)
    summe = np.sum(data, axis=1)[::-1]
    # summe_x = np.linspace(0,len(summe),len(summe))
    summe_x = np.linspace(extent[2], extent[3], len(summe))
    integralPlotx.clear()
    integralPlotx.get_xaxis().set_visible(False)
    integralPlotx.get_yaxis().set_visible(False)
    # integralPloty.set_xlim(0,np.shape(data)[0])
    # integralPlotx.set_ylim(0,np.shape(data)[0])
    integralPlotx.plot(summe, summe_x)

    # Finding start params for fit
    a = max(summe)
    x_0 = summe_x[summe.argmax()]
    sigma = 2

    a1 = max(summe[:(len(summe) / 2)])
    x1_0 = summe_x[summe[:(len(summe_x) / 2)].argmax()]
    a2 = max(summe[len(summe) / 2:])
    x2_0 = summe_x[summe[len(summe_x) / 2:].argmax() + len(summe) / 2]
    # sigma1 = sum(summe * (summe_x - mean1)**2)/len(summe_x) maybe???
    sigma1 = 2
    sigma2 = 2
    init_values_1 = [a1, x1_0, sigma1, a2, x2_0, sigma2]
    init_values_2 = [a, x_0, sigma]


    # print len(summe), a1, x1_0, a2, x2_0

    # fitting
    def doublegauss(summe_x, a1, x1_0, sigma1, a2, x2_0, sigma2):
        return a1 * exp(-(summe_x - x1_0) ** 2 / (2 * sigma1 ** 2)) + a2 * exp(
            -(summe_x - x2_0) ** 2 / (2 * sigma2 ** 2))


    def gauss(summe_x, a, x_0, sigma):
        return a * exp(-(summe_x - x_0) ** 2 / (2 * sigma ** 2))


    popt, pcov = curve_fit(doublegauss, summe_x, summe, p0=init_values_1)
    popt2, pcov2 = curve_fit(gauss, summe_x, summe, p0=init_values_2)

    # Distance:
    distance_4sigma = popt[4] - popt[1] - 2 * popt[2] - 2 * popt[5]
    distance_p2p = popt[4] - popt[1]
    # print(distance, popt[5], popt[2], popt[4], popt[1])








    db = doublegauss(summe_x, *popt)
    x_dip = 0
    sumx = summe_x.tolist()
    print('sumx is:')
    print(sumx)
    print(popt[1])
    print(popt[4])
    print(type(sumx))
    #print sumx
    #Compare values in the vicinity of the amplitude and chose the nearest to it
    diff1 = []
    diff2 = []
    #print(summe_x.tolist())
    for value in sumx:
        diff1.append(abs(value - popt[1]))
        diff2.append(abs(value - popt[4]))
    #print(diff1)
    #print(diff2)
    print(min(diff1))
    print(min(diff2))


    p1 = diff1.index(min(diff1))
    p2 = diff2.index(min(diff2))
    print(sumx[45])
    print(sumx[74])

# CONTROLL OUTPUT

    #print(type(p1))  #Which type does p1 and p2 have?
    #print(type(p2))
    print('Index of the nearest value to popt[1], p1:')
    print(p1)
    print('Index of the nearest value to popt[4], p2:')
    print(p2)


    print('Amplitude, a1:')
    print(a1)
    print('Amplitude, a2:')
    print(a2)
    print('Center, x1_0:')
    print(x1_0)
    print('Center, x2_0:')
    print(x2_0)
    print('Optimized, x2_0: Optimized, x1_0:')
    print(popt[4],popt[1])

    #int(sumx[p1]):int(sumx[p2]) wrong approach --> takes the int value of sumx index position instead of just the p1 and p2 index
    print(db[p1:p2])
    dip_value = min(db[p1:p2])
    print('dip_value:')
    print(dip_value)
    #print(db)
    for index, yvalue in np.ndenumerate(db):
        #print(index, yvalue)
        if dip_value == yvalue:
            x_dip = sumx[index[0]]
            #print(index[0])
        print(index, yvalue)
    print('yvalue:')
    print(yvalue)
    print('x_dip:')
    print(x_dip)
    print('dip_value:')
    print(dip_value)
    print('Values of db(optimized doublegauss fit):')
    pprint.pprint(db)







    # a1, x1_0, sigma1, a2, x2_0, sigma2
    # differs between doublegauss and gauss plots by checking for negative/positive 4sigma distance

    # if distance_4sigma >= 0:
    integralPlotx.plot(doublegauss(summe_x, *popt), summe_x,
                       'r-')  # , label='fit: a1=%5.3f, x1_0=%5.3f, sigma1=%5.3f, a2=%5.3f x2_0=%5.3f, sigma2=%5.3f' % tuple(popt))
    integralPlotx.plot(doublegauss(summe_x, *popt), summe_x, 'r-')  # , label="distance_4sigma=%5.1f" %distance_4sigma)
    integralPlotx.plot(doublegauss(summe_x, *popt), summe_x, 'r-', dip_value, x_dip, 'go')

    # label = 'fit: a1=%5.3f, x1_0=%5.3f, sigma1=%5.3f, a2=%5.3f x2_0=%5.3f, sigma2=%5.3f' % tuple(popt)
    # else:
    # integralPlotx.plot(gauss(summe_x, *popt2), summe_x, 'r-',  label='fit: a=%5.3f, x_0=%5.3f, sigma=%5.3f' % tuple(popt2))
    # label = 'fit: a=%5.3f, x_0=%5.3f, sigma=%5.3f' % tuple(popt2)

    # calculates the minimal value between the two center points of the doublegauss fit
    # print(type(integralPlotx.plot(doublegauss(summe_x, *popt), summe_x, 'r-', label='fit: a1=%5.3f, x1_0=%5.3f, sigma1=%5.3f, a2=%5.3f x2_0=%5.3f, sigma2=%5.3f' % tuple(popt))))

    # print(summe_x[int(x1_0):int(x2_0)])

    # xenum = []
    # for c, x_value in enumerate(summe_x):
    #     xenum.append((c,x_value))
    # print(xenum)
    # dip_value = min(x1_0,x2_0)

    # takes every paramter and puts it in an excel spreadsheet with its corresponding value; _wiki: puts it in a table format for easy copy paste input

    param_list = ['distance_4sigma', 'distance_p2p', 'Amplitude, a1', 'Center, x1_0', 'sigma1', 'Amplitude,a2',
                  'Center,x2_0', 'sigma2', 'Amplitude,a', 'Center', 'Sigma', 'dip_value']

    param_values = [distance_4sigma, distance_p2p] + popt.tolist() + popt2.tolist() + [dip_value]

    param_list_wiki = ['||', 'distance_4sigma', '||', 'distance_p2p', '||', 'Amplitude, a1', '||', 'Center, x1_0', '||',
                       'sigma1', '||', 'Amplitude,a2',
                       '||', 'x2_0', '||', 'sigma2', '||', 'Amplitude,a', '||', 'Center', '||', 'Sigma', '||',
                       'dip_value']

    param_values_wiki = ['||', distance_4sigma, '||', distance_p2p, '||', a1, '||', x1_0, '||', sigma1, '||', a2, '||',
                         x2_0, '||', sigma2, '||', a, '||', x_0, '||', sigma, '||']

    # print(param_list)
    # print(param_values)
    data_output(savePath + outName, param_list, param_values)
    data_output_2(savePath + outName, param_list_wiki, param_values_wiki)


    if showPlots:
        p.tight_layout()
        p.legend()
        #p.show()
    if saveResults:
        # p.text(20,20, label)
        p.savefig(os.path.join(savePath, outName + ".png"))
