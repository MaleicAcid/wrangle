import os,sys
import optparse

os.sys.path.insert(0, os.path.dirname(__file__)+"../CGDataNew")

from flattenClinical import *

onlyGenomicSamples =1
# 1 (default) only keep genomicSamples
# 0 keep all samples mentioned in both clinical and genomic data files

REALRUN = 1
#1 : full
#0 : clinical data only, full json
# -1: only copy genomic JSON, no clinical json and no probeMap json
# -2: only clinical feature data

parser = optparse.OptionParser()
parser.add_option("--inDir", action="store", type="string", dest="inDir")
parser.add_option("--outDir", action="store", type="string", dest="outDir")
parser.add_option("--sampleMap", action="store", type="string", dest="sampleMap")
(options, args) = parser.parse_args()

#print options

def printUsage():
    print "python runFlatten.py --inDir=inputDir --outDir=outputDir\n"
    print "options:"
    print "          --sampleMap=sampleMap"


if options.inDir==None or options.outDir ==None:
    printUsage()
    sys.exit()


inDir = options.inDir
outDir =options.outDir

if string.find(inDir, "~")!=-1 or string.find(outDir, "~")!=-1:
    print "do not use ~ in path"
    sys.exit()

if inDir[-1]!="/":
    inDir = inDir +"/"

if outDir[-1]!="/":
    outDir = outDir +"/"

r = runFlatten(inDir, outDir,REALRUN, onlyGenomicSamples, options.sampleMap)

