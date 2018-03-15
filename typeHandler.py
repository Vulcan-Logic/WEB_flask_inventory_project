'''
Created on 22-Dec-2017

@author: vineet
'''
from templating import Handler1
from dbProductType import TypeQuery
import json
import datetime

    
class catType(): 
    def put(self,parentKey,typeCode,typeDesc):
        retList=None
        if parentKey!="0":
                returnVal=TypeQuery().addType(typeCode=typeCode,
                                   typeDefinition=typeDesc,
                                   parentKey=parentKey)
        else:
                returnVal=TypeQuery().addType(typeCode=typeCode,
                                   typeDefinition=typeDesc)
        if returnVal is not None:
            types=TypeQuery().getChildTypesByKey(key=parentKey)            
            retCount=len(types)
            if retCount!=0:
                retString=json.dumps(types)
            else: 
                retString="" 
            retList=json.dumps({"count":retCount,"list":retString})  
        else:
            raise Exception(500,"Server Error: Unable to insert type")            
        return(retList)
    
    def checkDesc(self,parentId,desc):
        #returns true if description does not exist
        if TypeQuery().checkDesc(parentId, desc):
            return(True)
        else:
            return(False)
    #returns true if code does not exist
    def checkCode(self,parentId,code):
        if TypeQuery().checkCode(parentId,code):
            return(True)
        else:
            return(False)

    def getChildList(self,keyUrl):
        #return json 
        types=TypeQuery().getChildTypesByKey(key=keyUrl)
        retList=None
        if types is not None:
            retCount=len(types)
            if retCount!=0:
                retString=json.dumps(types)
            else: 
                retString="" 
            retList=json.dumps({"count":retCount,"list":retString})  
        else:
            raise Exception(500,"Server Error: Unable to get types")
        return(retList)


    def getCounterValue(self,keyUrl):
        counter=TypeQuery().getCounterByKey(keyUrl)
        if counter is not None:
            return(json.dumps({"counter":counter}))
        else:
            raise Exception(500,"Server Error: Unable to return counter value")


    
#obsolete or not used
class initialAddtype(Handler1):
    def get(self):
        self.render("addInitialTypes.html")

    
    def post(self):
        typeDesc=self.request.get("Desc")
        tCode=self.request.get("Code").strip()
        print(tCode)
        TypeQuery().addType(typeCode=tCode,typeDefinition=typeDesc)
        self.render("addInitialTypes.html")


class getStarterTypesJSON(Handler1):
    def get(self):
        returnedTypes=TypeQuery().getChildTypesByKey()
        retString=returnedTypes
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.status_int = 200
        self.response.out.write(json.dumps(retString))


class getStarterTypes(Handler1):
    def get(self):
        self.render("starterTest.html")

            
def filter_results(qry):
    """
    Send NDB query result to serialize function if single result, 
    else loop through the query result and serialize records one by one
    """
    result = []

    # check if qry is a list (multiple records) or not (single record)
    if type(qry) != list:
        record = make_ndb_return_data_json_serializable(qry)
        return(record)

    for q in qry:
        result.append(make_ndb_return_data_json_serializable(q))

    return(result)


def make_ndb_return_data_json_serializable(data):
    """Build a new dict so that the data can be JSON serializable"""
    
    result = data.to_dict()
    record = {}

    # Populate the new dict with JSON serializiable values
    for key in result.iterkeys():
        if isinstance(result[key], datetime.datetime):
            record[key] = result[key].isoformat()
            continue
        record[key] = result[key]
    
    # Add the key so that we have a reference to the record
    record['key'] = data.key.id()
    return(record)





            