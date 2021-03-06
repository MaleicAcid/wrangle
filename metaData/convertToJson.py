import string, sys
import json
import xena_query as xena

if len(sys.argv[:]) != 3:
    print "python convertToJson.py input_default_txt json_output"
    sys.exit()

input = sys.argv[1]
fin = open(input,'U')
output = sys.argv[2]
fout = open(output,'w')

#hub
line = fin.readline()
hub = string.strip(line)

#header
line = fin.readline()
headers = string.split(line[:-1],'\t')[1:]

J={}
for line in fin.readlines():
    list = string.split(string.strip(line),'\t')
    cohort = list[0]
    datasets = list[1:]
    #print headers
    #print datasets
    J[cohort]={}
    for i in range (0, min(len(headers), len(datasets))):
        header = headers[i]
        dataset = datasets[i]
        if dataset == "":
            continue

        J[cohort][header] = {}
        J[cohort][header]['host'] = hub
        J[cohort][header]['dataset'] = dataset
fout.write(json.dumps( J, indent= 4 ))
fin.close()
fout.close()
