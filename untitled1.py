#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 01:15:50 2020

@author: sunnywang
"""


import re
import operator
import csv

error={}
per_user={}
userInfo={}
usererr={}

with open("syslog.log","r") as file:
        lines=file.readlines();
        for line in lines:
                resErr=re.search(r"ticky: ERROR ([\w ]*).*\(([\w\.]*)\)", line)
                resInfo=re.search(r"ticky: INFO ([\w ]*).*\(([\w\.]*)\)", line)
                if resErr:
                    if len(resErr.groups())>0:
                        if resErr.groups()[0] in error:
                            error[resErr.groups()[0]]+=1
                        else:
                            error[resErr.groups()[0]]=1
                    if len(resErr.groups())>1:
                        if resErr.groups()[1] in usererr:
                            usererr[resErr.groups()[1]]+=1
                        else:
                            usererr[resErr.groups()[1]]=1
                    
                    #per_user[resErr[2]][0]+=1
                if resInfo:
                    if len(resInfo.groups())>1:
                        #print(resInfo.groups()[1])
                        if resInfo.groups()[1] in userInfo:
                        #if resInfo[2] in userInfo:
                            userInfo[resInfo.groups()[1]]+=1
                        else:
                            userInfo[resInfo.groups()[1]]=1
def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {}
   for key, value in dict1.items():
       if key in dict1 and key in dict2:
           dict3[key] = [dict1[key] , dict2[key]]
       else:
           dict3[key] = [dict1[key] , 0]
   for key, value in dict2.items():
       if key in dict1 and key in dict2:
           #dict3[key] = [dict1[key] , dict2[key]]
           pass
       else:
           dict3[key] = [0 , dict2[key]]
 
   return dict3

per_user=mergeDict(userInfo,usererr)

lsterr=[]
lsterr=sorted(error.items(), key=operator.itemgetter(1), reverse=True)

fieldnames = ['Error','Count']
with open('error_message.csv', 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(fieldnames)
    for item in lsterr:
        writer.writerow([item[0],item[1]])


lstuser=[]
lstuser=sorted(per_user.items(), key=operator.itemgetter(0))

userfieldnames = ['UserName','Info','Error']
with open('user_statistics.csv', 'w', newline="") as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(userfieldnames)
    for item in lstuser:
        writer.writerow([item[0],item[1][0],item[1][1]])

                        