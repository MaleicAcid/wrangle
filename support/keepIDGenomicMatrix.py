import string, sys,os

def listing (mfile):
    fin = open(mfile,'r')
    list =[]
    for line in fin.readlines():
        data = string.strip(line)
        if data not in list:
            list.append(data)
    fin.close()
    return list

def keepIDs (inputFile, outputFile, keep_list):
    fin = open(inputFile,'U')

    goodPos=[]
    ids = string.split(fin.readline()[:-1],'\t')
    for i in range (0, len(ids)):
        if ids[i] in keep_list:
            goodPos.append(i)
            print ids[i], i
    fin.close()

    goodPos.sort()
    s= "cut -f 1,"  #pos=0 always in
    for i in goodPos[:-1]:
        s= s+str(1+i)+","
    s = s + str(1+goodPos[-1]) + " " +inputfile +" > " + outputFile
    os.system(s)

if len(sys.argv[:])!=4:
    print "python keepIDGenomicMatrix.py matrixfile output keep_list(one_id_per_line)"
    sys.exit()

listfile = sys.argv[3]
keep_list  = listing (listfile)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

keepIDs (inputfile, outputfile, keep_list)
