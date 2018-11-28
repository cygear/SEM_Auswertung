import os

datapath = "/home/johannes/Current_Data/SEM_Data_2018_10_17&18/"
position = 28000
for i in range(4):
    os.makedirs(os.path.join(datapath + 'minus' + str(position + i * 1000) + '_Auswertung'))
