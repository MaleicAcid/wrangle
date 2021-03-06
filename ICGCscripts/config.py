import urllib2,sys,json

bigDir = "/inside/depot/icgcFiles/"
#bigDir = "/mnt/test/icgcFiles/"
smallDir = "/data/TCGA/icgcFiles/"
#smallDir = "/mnt/test/icgcFiles/"
release = "release_22"

MAX_projects =100

icgcDataTypes = [ # only the dataset types of interest
    #'sample',
    #'specimen',
    #'donor',
    #'donor_exposure',
    #'donor_family',
    #'donor_therapy',

    #'exp_array',
    #'mirna_seq',
    #'meth_array',
    #'meth_seq',

    #'copy_number_somatic_mutation',
    #'exp_seq',
    #'protein_expression',
    'simple_somatic_mutation.open',
    #'structural_somatic_mutation',
    #'splice_variant'
]

def getProjects():
    projects=[]
    url = 'https://dcc.icgc.org/api/v1/projects?size='+ str(MAX_projects)
    response = urllib2.urlopen(url).read()
    J= json.loads(response)
    print len(J['hits'])
    for hit in J['hits']:
        projects.append(hit['id'])
    return projects

def getPrimarySite():
    projects = getProjects()
    dic={}
    for p in projects:
        url = 'https://dcc.icgc.org/api/v1/projects/'+p
        response = urllib2.urlopen(url).read()
        J= json.loads(response)
        try:
            dic [p]= J["primarySite"]
        except:
            dic[p]=""
    return dic

def getPrimaryDisease():
    projects = getProjects()
    dic={}
    for p in projects:
        url = 'https://dcc.icgc.org/api/v1/projects/'+p
        response = urllib2.urlopen(url).read()
        J= json.loads(response)
        try:
            disease = J["tumourType"]
        except:
            disease =""

        try:
            disease = disease +" : "+J["tumourSubtype"]
        except:
            pass
        dic[p]=disease
    return dic

