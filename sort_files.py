# sort_files.py - This programm takes directories and sorts their content according to slices of their names

import os
import pprint
import shutil
import glob

# Enter a filepath:
file_path = glob.glob("/home/johannes/Current_Data/SEM_Data_2018_10_17&18/*/")
#folder_list = os.listdir(file_path)


# Slices
# pprint.pprint(file_list)
def sort_by_chars(x, a, b):
    return (x[a:b])


# TODO: How to the function 'sort_by_chars' give the slices of the filenames as a key value to the sorted function?
# Answer: The function 'sort_by_chars' doesnt take the list variable but the items of the list variable seperately and compares their slice values

# a = -4
# b = -1
# sorted(folder_list, key=lambda folder_list, a=5, b=9: sort_by_chars(folder_list, a,
#                                                                     b))  # sorts the given listed folders according to the chosen slice of chars
# pprint.pprint(sorted(folder_list, key=lambda folder_list, a=5, b=9: sort_by_chars(folder_list, a, b)))
#
# # sorts files into fitting folders
#
# for folder in sorted(folder_list, key=lambda folder_list, a=5, b=9: sort_by_chars(folder_list, a, b)):
#     file_list = os.listdir(file_path + '/' + folder)
#     pprint.pprint(sorted(file_list, key=lambda file_list, a=10, b=12: sort_by_chars(file_list, a, b)))

#Sortieralgorithmus ist sehr fallspezifisch. Allgemeinere Eingabemethode finden

destiny = "/home/johannes/Current_Data/SEM_Auswertung_gausskasten_2018_10_17&18/"

for file in file_path:
    #print file
    data_list = os.listdir(file)
    for i in range(len(data_list)):
        if '0_1000mV' in data_list[i]:
            shutil.move(file + data_list[i], destiny + '0_1000mV/' )
        elif '1_500mV' in data_list[i]:
            shutil.move(file + data_list[i], destiny + '1_500mV/' )
        elif '2_250mV' in data_list[i]:
            shutil.move(file + data_list[i], destiny + '2_250mV/' )
        else:
            shutil.move(file + data_list[i], destiny + '4_150mV/')
