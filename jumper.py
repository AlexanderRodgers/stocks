import os
import time
import csv

os.chdir(os.getcwd() + '\\stock_dfs\\')
for dirc in os.walk(os.getcwd(), topdown=True):
    for comps in dirc[2]:
        with open(comps, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            firstline = True
            things = []
            for row in reader:
                if firstline:
                    firstline = False
                    continue
                #Stopped here.
