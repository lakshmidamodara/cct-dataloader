import sys
import subprocess
import io
import openpyxl

#with open("A.csv", "a") as f:
#    f.flush()
#    sub.Popen(["cat", "A.csv"], stdout=f)

#p = sub.Popen(["type", "A.csv"], stdout=sub.PIPE, stderr=sub.PIPE)
#result = p.communicate()
#print(result)

filename = "Bayshore A-Mechanical Tracker v5.xlsx"

test = subprocess.Popen(['powershell', '/C', 'cat "Bayshore A-Mechanical Tracker v5.xlsx" '], stdout=subprocess.PIPE)
out, err = test.communicate()
print( out)

