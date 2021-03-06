import os,string,sys
import copy
import re

from CGDataUtil import *

class ClinicalFeatureNew():
    def __init__ (self, rFHandle,name):
        # return emptySelf if fail to initiate
        self.__name=""
        self.__FEATUREs=[]
        self.__DATA={}
        self.__CONTROLVOC =["shortTitle","longTitle",
                            "valueType","state","stateOrder",
                            "stateOrderRelax",
                            "sameAs",
                            "priority","visibility"]
        
        emptySelf =copy.deepcopy(self)
        self.__name=name
        self.__VALID=0
        
        if rFHandle ==None:
            return
        
        try:
            rFHandle+"a"
            readHandle=open(rFHandle,'r')
        except TypeError:
            readHandle=rFHandle

        # load data
        for line in readHandle.readlines():
            if string.strip(line)=="":
                continue
            data = string.split(line[:-1],"\t")
            if len(data)!=3:
                print "not 3 fields",data
                self=emptySelf
                return
            feature = string.strip(data[0])
            if feature =="":
                continue
            #ignore _PATIENT feature
            #if feature =="_PATIENT":
            #    continue
            key = string.strip(data[1])
            value = string.strip(data[2])
            if key =="" or value =="":
                continue
            if  key not in self.__CONTROLVOC:
                continue
            if feature not in self.__FEATUREs:
                self.__FEATUREs.append(feature)
                self.__DATA[feature]={}

            if self.__DATA[feature].has_key(key):
                if key == "state":
                    if  value not in self.__DATA[feature][key]:
                        if len(value)>=3 and value[0]=="\"" and value[-1]=="\"":
                            self.__DATA[feature][key].append(value[1:-1])
                        else:
                            self.__DATA[feature][key].append(value)
                else:
                    continue
            else:
                if key == "state":
                    if len(value)>=3 and value[0]=="\"" and value[-1]=="\"":
                        self.__DATA[feature][key]=[value[1:-1]]
                    else:
                        self.__DATA[feature][key]=[value]
                elif key=="stateOrder":
                    if value[0]!="\"" or value[-1]!="\"":
                        print "In stateOrder, each state needs to be in quote", value
                        self=emptySelf
                        return
                    orders = string.split(value[1:-1],"\"")
                    if len(orders) %2 != 1:
                        print "Error in stateOrder", value
                        self=emptySelf
                        return
                    self.__DATA[feature]["stateOrder"]=[]
                    for i in range (0, len(orders),2):
                        if orders[i] not in self.__DATA[feature]["stateOrder"]:
                            self.__DATA[feature]["stateOrder"].append(orders[i])
                else:
                    self.__DATA[feature][key]=value

        readHandle.close()
        # need validation?
        self.__VALID=1
        return

    def isValid(self):
        return self.__VALID

    def getShortTitle(self,feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("shortTitle"):
                return self.__DATA[feature]["shortTitle"]
        else:
            return None

    def getLongTitle(self, feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("longTitle"):
                return self.__DATA[feature]["longTitle"]
        else:
            return None

    def getValueType(self, feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("valueType"):
                return self.__DATA[feature]["valueType"]
        else:
            return None

    def getStates(self, feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("state"):
                return self.__DATA[feature]["state"]
        else:
            return None

    def getStateOrder(self, feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("stateOrder"):
                return self.__DATA[feature]["stateOrder"]
        else:
            return None

    def getStateOrderRelax(self, feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("stateOrderRelax"):
                return self.__DATA[feature]["stateOrderRelax"]
        else:
            return None

    def getFeatureSameAs(self,feature):
        if feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("sameAs"):
                return self.__DATA[feature]["sameAs"]
        else:
            return None
        
    def getFeatures(self):
        return copy.deepcopy(self.__FEATUREs)

    def addFeature (self, feature):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
            self.__FEATUREs.append(feature)

    def setFeatureShortTitle(self, feature, shortTitle):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
            self.__FEATUREs.append(feature)
        self.__DATA[feature]["shortTitle"]= shortTitle
        return True
    
    def setFeatureLongTitle(self, feature, longTitle):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
            self.__FEATUREs.append(feature)
        self.__DATA[feature]["longTitle"]= longTitle
        return True

    def setFeaturePriority(self, feature, priority):
        if feature not in self.__FEATUREs:
            return False
        self.__DATA[feature]["priority"]= priority
        return True

    def setFeatureVisibility(self, feature, visibility):
        if feature not in self.__FEATUREs:
            return False
        if visibility not in ["on","off"]:
            return False
        self.__DATA[feature]["visibility"]= visibility
        return True
    
    def setFeatureValueType(self, feature, valueType):
        if valueType not in ["category","float"]:
            return False
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
            self.__FEATUREs.append(feature)
        self.__DATA[feature]["valueType"]= valueType
        return True

    def setFeatureStates(self, feature, states):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
        if (not self.__DATA[feature].has_key("valueType")) or self.__DATA[feature]["valueType"]!="category":
            return False
        self.__DATA[feature]["state"]= states
        return True

    def setFeatureStateOrder(self, feature, stateOrder):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
        if (not self.__DATA[feature].has_key("valueType")) or self.__DATA[feature]["valueType"]!="category":
            return False
        if (not self.__DATA[feature].has_key("state")):
            return False
        self.__DATA[feature]["stateOrder"]= stateOrder
        return True

    def setFeatureStateOrderRelax(self, feature, bvalue):
        if feature not in self.__FEATUREs:
            self.__DATA[feature]={}
        if self.__DATA[feature]["valueType"] not in ["category"]:
            return False
        if bvalue not in ["true"]:
            return False
        self.__DATA[feature]["stateOrderRelax"]= bvalue
        return True

    def cleanState(self):
        removeF =[]
        for feature in self.__FEATUREs:
            states = self.getStates(feature)
            if states ==None:
                continue
            newStates =[]
            strStates=[]
            for state in states:
                if state != "":
                    newStates.append(state)
            sort_nicely(newStates)
            
            if len(newStates)==0:
                self.__DATA[feature].pop("state")
                self.__DATA[feature].pop("stateOrder")
                self.__DATA[feature].pop("valueType")
                if len(self.__DATA[feature].keys())==0:
                    removeF.append(feature)
            elif states != newStates:
                self.__DATA[feature]["state"]=newStates
                self.__DATA[feature]["stateOrder"]=="\""+string.join(newStates,"\",\"")+"\""
            else:
                pass
        for feature in removeF:
            print "pop from clinicalFeature due to empty state", feature
            self.__DATA.pop(feature)
            self.__FEATUREs.remove(feature)
            
    def removeFeatures(self, features):
        for feature in features:
            if feature not in self.__FEATUREs:
                continue
            self.__DATA.pop(feature)
            self.__FEATUREs.remove(feature)

    def replaceFeatureName(self, oldName, newName):
        if oldName ==newName:
            return
        if newName in self.__FEATUREs:
            return
        if oldName not in self.__FEATUREs:
            return

        print oldName
        self.__DATA[newName]=copy.deepcopy(self.__DATA[oldName])
        self.__DATA.pop(oldName)
        self.__FEATUREs.append(newName)
        self.__FEATUREs.remove(oldName)

    def replicateFeatureName(self, oldName, newName):
        if oldName ==newName:
            return
        if newName in self.__FEATUREs:
            return
        if oldName not in self.__FEATUREs:
            return

        print oldName
        self.__DATA[newName]=copy.deepcopy(self.__DATA[oldName])
        #self.__DATA.pop(oldName)
        self.__FEATUREs.append(newName)
        #self.__FEATUREs.remove(oldName)

    def checkFeatureWithMatrix(self,cMa):
        cMaFeatures = cMa.getCOLs()
        removeF=[]
        for feature in self.__FEATUREs:
            if feature not in cMaFeatures:
                removeF.append(feature)
                print "feature not in matrix file",feature
                continue
            if self.__DATA[feature].has_key("valueType") and self.__DATA[feature]["valueType"]=="category" : #suppose to be category
                if cMa.isTypeCategory (feature)==False and cMa.isTypeInt (feature) ==False:
                    if self.__DATA[feature].has_key("state"):
                        self.__DATA[feature].pop("state")
                    if self.__DATA[feature].has_key("stateOrder"):
                        self.__DATA[feature].pop("stateOrder")
                    self.__DATA[feature].pop("valueType")
                    if len(self.__DATA[feature].keys())==0:
                        removeF.append(feature)
                elif self.__DATA[feature].has_key("state") or self.__DATA[feature].has_key("stateOrder"):  

                    #check all catorical state values match what is the matrix
                    cMaStates= cMa.getColStates(feature)
                    states = copy.deepcopy(self.getStates(feature))

                    #relaxed version state and stateOrder can have extra value, matrix can have extra value, extra vlue of matrix is added to the end of the ordering.
                    if self.__DATA[feature].has_key("stateOrderRelax"):
                        print feature,"relax"
                        edit=0
                        for state in cMaStates:
                            if state not in states:
                                self.__DATA[feature]["state"].append(state)
                                self.__DATA[feature]["stateOrder"].append(state)
                                print "WARNING: not all matrix state in feature state, add new states at the end"
                                #print "WARNING: not all matrix state in feature state, reset new state new stateOrder"
                                #edit=1
                                #break
                        """
                        if (edit):
                            self.__DATA[feature]["state"]=[]
                            for state in cMaStates:
                                if state not in self.__DATA[feature]["state"]:
                                    self.__DATA[feature]["state"].append(state)
                            sort_nicely(cMaStates)
                            self.__DATA[feature]["stateOrder"]=cMaStates
                        """
                    #strict version state and stateOrder can not have extra value that is not in matrix, neither is matrix, must perfectly match
                    else:
                        print feature,"not relax"
                        print self.__DATA[feature]
                        # remove extra from clinicalFeature
                        for state in states:
                            if state not in cMaStates:
                                print "WARNING pop from clinicalFeature", feature, state
                                self.__DATA[feature]["state"].remove(state)
                        states = copy.deepcopy(self.getStates(feature))
                        if len(cMaStates)!= len(self.getStates(feature)):
                            print "WARNING: not all matrix state in feature state, reset new state new stateOrder"
                            print "WARNING:", self.__name, feature, "matrix:", cMaStates
                            print "WARNING:", self.__name, feature, "feature:", states
                            self.__DATA[feature].pop("state")
                            self.__DATA[feature].pop("stateOrder")
                            continue
                        #check stateOrder match matrix file, remove extra state from stateOrder if not in matrix file
                        order = copy.deepcopy(self.getStateOrder(feature))
                        for state in order:
                            if state not in cMaStates:
                                self.__DATA[feature]["stateOrder"].remove(state)
                        #check stateOrder match matrix file, if matrix state not in stateOrder, reset stateOrder
                        if len(cMaStates)!= len(self.getStateOrder(feature)):
                            print "WARNING not all matrix state in stateOrder, set new stateOrder"
                            print feature, "matirx", cMaStates
                            print feature, "oldfeature", self.getStateOrder(feature)
                            sort_nicely(cMaStates)
                            self.__DATA[feature]["stateOrder"]=cMaStates
                    #strict version

            """            
            elif self.__DATA[feature].has_key("valueType") and self.__DATA[feature]["valueType"]=="float" : #suppose to be float
                r = cMa.isTypeCategory (feature)
                if r==True:
                    self.__DATA[feature].pop("valueType")
                    if len(self.__DATA[feature].keys())==0:
                        removeF.append(feature)
            """
        self.removeFeatures(removeF)
        return

    def fillInFeaturesWithMatrix(self,cMa):
        allFeatures = cMa.getCOLs()
        for feature in allFeatures:
            if feature not in self.__FEATUREs:
                self.__FEATUREs.append(feature)
                self.__DATA[feature]={}
        return
    
    def fillInValueTypeWithMatrix(self,cMa):
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("valueType"):
                r = cMa.isTypeCategory (feature)
                if r == True : #category
                    self.__DATA[feature]["valueType"]="category"
                    states = cMa.getColStates(feature)
                    sort_nicely(states)
                    self.__DATA[feature]["state"]=states
                    self.__DATA[feature]["stateOrder"]=states
                else:
                    self.__DATA[feature]["valueType"]="float"
            elif not self.__DATA[feature].has_key("state") or not self.__DATA[feature].has_key("stateOrder"):
                states = cMa.getColStates(feature)
                sort_nicely(states)
                self.__DATA[feature]["state"]=states
                self.__DATA[feature]["stateOrder"]=states
        return
    
    def fillInTitles(self):
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("shortTitle"):
                self.__DATA[feature]["shortTitle"] = feature
            if not self.__DATA[feature].has_key("longTitle"):
                self.__DATA[feature]["longTitle"] = self.__DATA[feature]["shortTitle"]
        return
                
        #if no priority set, autoset priority based on UPPER CASE of shortTitle
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("shortTitle"):
                self.__DATA[feature]["shortTitle"] = feature
        sTitles =[]
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("priority"):
                sTitles.append(string.upper(self.__DATA[feature]["shortTitle"]))
        sTitles.sort()


    def fillInPriorityVisibility(self, VIS):
        visib=0
        for feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("visibility") and self.__DATA[feature]['visibility']=="on":
                visib= visib+1
            #elif not self.__DATA[feature].has_key("visibility"):
            #    self.__DATA[feature]["visibility"] = "off"

        #if no priority set, autoset priority based on UPPER CASE of shortTitle
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("shortTitle"):
                self.__DATA[feature]["shortTitle"] = feature
        sTitles =[]
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("priority"):
                sTitles.append(string.upper(self.__DATA[feature]["shortTitle"]))
        sTitles.sort()

        numPriority =[]
        for feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("priority"):
                numPriority.append(float(self.__DATA[feature]["priority"]))
        numPriority.sort()

        if len(numPriority)!=0:
            startPriority = int(numPriority[-1]+1)
        else:
            startPriority = 1

        if visib > VIS:  # too many feature has visibility on, set those without priority to off
            for feature in self.__FEATUREs:
                if self.__DATA[feature].has_key("visibility") and self.__DATA[feature]['visibility']=="on":
                    if not self.__DATA[feature].has_key("priority"):
                        self.__DATA[feature]["visibility"] = "off"
                        visib=visib-1
                        if visib <= VIS:
                            break

        if visib > VIS:  # too many feature has visibility on
            numPriorityR = copy.deepcopy(numPriority)
            numPriorityR.reverse()
            for p in numPriorityR:
                for feature in self.__FEATUREs:
                    if self.__DATA[feature].has_key("visibility") and self.__DATA[feature]["visibility"]=="on" and self.__DATA[feature].has_key("priority"):
                        if float(self.__DATA[feature]["priority"]) == p:
                            self.__DATA[feature]["visibility"] = "off"
                            visib=visib-1
                            if visib <= VIS:
                                break
                if visib <= VIS:
                    break

        if visib < VIS: #too few has visibilities
            for p in numPriority:
                for feature in self.__FEATUREs:
                    #if ((not self.__DATA[feature].has_key("visibility")) or (self.__DATA[feature].has_key("visibility") and self.__DATA[feature]["visibility"] =="off")) and self.__DATA[feature].has_key("priority"):  #no visi with prio
                    if (not self.__DATA[feature].has_key("visibility") ) and self.__DATA[feature].has_key("priority"):  #no visi with prio
                        if float(self.__DATA[feature]["priority"]) == p:
                            self.__DATA[feature]["visibility"] = "on"
                            visib=visib+1
                            if visib >= VIS:
                                break
                if visib >= VIS:
                    break
                    
        for feature in self.__FEATUREs:
            if not self.__DATA[feature].has_key("priority"):
                for i in range (0, len(sTitles)):
                    if string.upper(self.__DATA[feature]["shortTitle"]) == sTitles[i]:
                        self.__DATA[feature]["priority"] = str(startPriority + i)
            if not self.__DATA[feature].has_key("visibility"):
                if visib < VIS:
                    self.__DATA[feature]["visibility"] = "on"
                    visib=visib+1
                else:
                    self.__DATA[feature]["visibility"] = "off"
            else:
                if visib < VIS and self.__DATA[feature]["visibility"]!="off":
                    self.__DATA[feature]["visibility"] = "on"
                    visib=visib+1
        return
    
    def store(self, fout):
        fout.write("feature\tattribute\tvalue\n")
        for feature in self.__FEATUREs:
            if self.__DATA[feature].has_key("shortTitle"):
                fout.write(feature+"\tshortTitle\t"+self.__DATA[feature]["shortTitle"]+"\n")
            if self.__DATA[feature].has_key("longTitle"):
                fout.write(feature+"\tlongTitle\t"+self.__DATA[feature]["longTitle"]+"\n")
            if self.__DATA[feature].has_key("valueType") and self.__DATA[feature]["valueType"]=="category" : 
                fout.write(feature+"\tvalueType\tcategory\n")
                if self.__DATA[feature].has_key("state"):
                    for state in self.__DATA[feature]["state"]:
                        fout.write(feature+"\tstate\t"+str(state)+"\n")
                if self.__DATA[feature].has_key("stateOrder") and len(self.__DATA[feature]["stateOrder"]) >0:
                    fout.write(feature+"\tstateOrder\t")
                    for item in self.__DATA[feature]["stateOrder"][:-1]:
                        fout.write("\""+item+"\",")
                    fout.write("\""+self.__DATA[feature]["stateOrder"][-1]+"\"\n")
            if self.__DATA[feature].has_key("valueType") and self.__DATA[feature]["valueType"]=="float" : 
                fout.write(feature+"\tvalueType\tfloat\n")
            if self.__DATA[feature].has_key("stateOrderRelax"):
                fout.write(feature+"\tstateOrderRelax\t"+self.__DATA[feature]["stateOrderRelax"]+"\n")
            if self.__DATA[feature].has_key("sameAs"):
                fout.write(feature+"\tsameAs\t"+self.__DATA[feature]["sameAs"]+"\n")
        fout.close()
