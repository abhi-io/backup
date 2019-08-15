#
from tabula import *
import csv
from collections import defaultdict
import mysql.connector
print("[[[ started ]]]")
m_dict={}
# convert_into("B.TechHons.Results-2015admsn.-toPublish200719.pdf","testpdf.tsv",output_format="tsv",pages='1-29')
print("convertion complete")
d={}
i=1

with open("testpdf.tsv") as f:
    for line in f:
        key=line.split()
        aa=(key[-1])
        if ((len(key[-1]))==10 or (len(key[-1]))==11):
            # print("-",key[-1])
            aa=key[-1]
            # print(aa[-2:])
            if(aa[-2:].isnumeric()):
                                                                    # if (len(aa)==10 or (len(aa))==11):
                                                                    #     if((aa[0])=='L'):
                                                                    #         my_list.append(i)
                clg=aa[:3]
                yr=aa[3:5]
                br=aa[5:7]
                rl=aa[7:10]
                print(i,">",key[-1],clg,yr,br,rl)
                i+=1
