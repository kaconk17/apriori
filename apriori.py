#source : https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/

import pyodbc
from apyori import apriori
import configparser
import os

conf = configparser.RawConfigParser()
fileDir = os.path.dirname(__file__)
file_name = "env.cfg"
confPath = os.path.join(fileDir, file_name)
conf.read(confPath)


server = conf.get("config", "server")
database = conf.get("config", "db")
username = conf.get("config", "user")
password = conf.get("config", "pass")

print("==============Apriori==================")
supp = float(input("Masukkan nilai support......%  "))
confidence = float(input("Masukkan nilai Confidence.......%  "))

supp = supp / 100.0
confidence = confidence /100.0

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)

cursor = cnxn.cursor()

cursor.execute("SELECT kd_brg = STUFF((SELECT ', ' + kd_brg FROM tb_data as b WHERE b.nota = a.nota FOR XML PATH('')), 1, 2, '') FROM tb_data as a GROUP BY nota")

records = []
for row in cursor :
    rowdat = str(row[0])
    l = rowdat.split(', ')
    records.append(l)

association_rules = apriori(records, min_support=supp, min_confidence = confidence, min_lift=0.2, min_length=3)
association_result = list(association_rules)
#print(len(association_result))
if len(association_result)<=0:
    print("Support atau Confidence terlalu tinggi !")
else:
    for item in association_result :
        pair = item[0]
        items = [x for x in pair]
        print("Kode Barang: " + items[0] + " -> " + items[1])
        
        print("Support: " + str(item[1]))
        print("Confidence: " + str(item[2][0][2]))
        print("Lift: " + str(item[2][0][3]))
        print("=====================================")

