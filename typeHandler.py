'''
Created on 22-Dec-2017

@author: vineet
'''
from templating import Handler1
from dbProductType import TypeQuery
import json
import datetime


class getStarterTypesJSON(Handler1):
    def get(self):
        returnedTypes=TypeQuery().getTypesByParent("0")
        print(returnedTypes)
        retString=returnedTypes
        print(json.dumps(retString))
        self.response.out.headers['Content-Type'] = 'text/json'
        self.response.status_int = 200
        self.response.out.write(json.dumps(retString))


class getStarterTypes(Handler1):
    def get(self):
        self.render("starterTest.html")

    
class insertType(Handler1): 
    def post(self):
        parentId=self.request.get("parentId")
        typeDesc=self.request.get("Desc")
        typeCode=self.request.get("Code")
        parentId=int(parentId)
        print('parent id is ')
        print(parentId)
        if parentId!=0:
                returnVal=TypeQuery().addType(typeCode=typeCode,
                                   typeDefinition=typeDesc,
                                   parentId=parentId)
        else:
                returnVal=TypeQuery().addType(typeCode=typeCode,
                                   typeDefinition=typeDesc)
        if returnVal is not None:
            types=TypeQuery().getTypesByParentId(parentId=parentId)
            if types is not None:
                if types==0:
                    retCount=0
                    retString=("")
                else:
                    retCount=len(types)
                    retString=json.dumps(types) 
                retList=json.dumps({"count":retCount,"list":retString})  
                self.response.out.headers['Content-Type'] = 'text/json'
                self.response.status_int = 201
                self.response.out.write(retList)
        else:
            self.response.headers['Content-Type'] = 'application/text'
            self.response.status_int = 500
            self.response.out.write("")

           
class initialAddtype(Handler1):
    def get(self):
        self.render("addInitialTypes.html")

    
    def post(self):
        typeDesc=self.request.get("Desc")
        tCode=self.request.get("Code").strip()
        print(tCode)
        TypeQuery().addType(typeCode=tCode,typeDefinition=typeDesc)
        self.render("addInitialTypes.html")
 

class validateTypeDesc(Handler1):
    def get(self):
        parentId=self.request.get("parentId")
        desc=self.request.get("Desc")
        self.response.out.headers['Content-Type'] = 'application/text'
        self.response.status_int = 200
        if TypeQuery().checkDesc(parentId, desc):
            self.response.out.write("1")
        else:
            self.response.out.write("0")

        
class validateTypeCode(Handler1):
    def get(self):
        parentId=self.request.get("parentId")
        code=self.request.get("code")
        self.response.out.headers['Content-Type'] = 'application/text'
        self.response.status_int = 200
        if TypeQuery().checkCode(parentId, code):
            self.response.out.write("1")
        else:
            self.response.out.write("0")

   
class getTypeList(Handler1):
    def get(self):
        #return json 
        keyUrl=self.request.get('kId')
        types=TypeQuery().getTypesByParent(parentKey=keyUrl)
        if types is not None:
            retCount=len(types)
            print("in getTypeList: ListCount")
            print(retCount)
            if retCount!=0:
                retString=json.dumps(types)
            else: 
                retString="" 
            retList=json.dumps({"count":retCount,"list":retString})  
            self.response.out.headers['Content-Type'] = 'text/json'
            self.response.status_int = 200
            self.response.out.write(retList)
        else:
            self.response.headers['Content-Type'] = 'application/text'
            self.response.status_int = 500
            self.response.out.write("")
    
            
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


            