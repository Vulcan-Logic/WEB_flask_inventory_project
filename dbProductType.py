'''
Created on 22-Dec-2017

@author: vineet
'''

from google.appengine.ext import ndb
import json
import datetime

class ProductType(ndb.Model):
    typeCode=ndb.StringProperty(required=True) #for SKU code
    typeDefinition=ndb.StringProperty(required=True) 
    level=ndb.IntegerProperty()
    counter=ndb.IntegerProperty()
    dateModified=ndb.DateTimeProperty(auto_now=True)
    modifiedBy=ndb.KeyProperty()
    
class TypeQuery():
    
    def addType(self,typeCode,typeDefinition,parentId=None):
        if parentId is not None:
            parentId=int(parentId)
            parentType=self.getTypeById(parentId)
            print("in addType")
            print(parentType)
            if parentType is not None:
                parentKey=ndb.Key('ProductType',parentId)
                typeEntry=ProductType(typeCode = typeCode.upper(), 
                                    counter = 0,
                                    level = parentType.level+1, 
                                    typeDefinition = typeDefinition.upper(),
                                    parent = parentKey)
                returnKey = typeEntry.put()
            else: 
                return(None)
        else:
            parentKey=ndb.Key('ProductType',"0")      
            typeEntry=ProductType(typeCode = typeCode, 
                                counter = 0, 
                                level=0,
                                typeDefinition = typeDefinition,
                                parent = parentKey)
            returnKey = typeEntry.put()
        if returnKey is not None:
            return(returnKey)
        else:
            return(None)
    
    
    def getTypesByParent(self,parentKey=None):#fetch types by parent
        if parentKey is not None:
            if parentKey=="0":
                parentKey=ndb.Key('ProductType',"0")
            else:
                parentKey=ndb.Key(urlsafe=parentKey)
            query=ProductType().query(ancestor=parentKey).order(
                                                ProductType.dateModified)
            returnList=[]
            if query.count()>0:
                results=query.fetch()
                for result in results:
                    listElement={ 
                                 'key': result.key.urlsafe(),
                                 'typeCode': result.typeCode,
                                 'typeDefinition':result.typeDefinition,
                                 'level':result.level
                        }
                    returnList.append(listElement)
            return(returnList)
        else:            
            return(None)
                
    def getTypesByParentId(self,parentId=None):#fetch types by parent
        if parentId is not None:
            if parentId==0:
                parentKey=ndb.Key('ProductType',"0")
            else:
                parentId=int(parentId)
                parentKey=ndb.Key('ProductType',parentId)
                
            query=ProductType().query(ancestor=parentKey).order(
                                                ProductType.dateModified)
            returnList=[]
            if query.count()>0:
                results=query.fetch()
                for result in results:
                    listElement={ 
                                 'key': result.key.urlsafe(),
                                 'typeCode': result.typeCode,
                                 'typeDefinition':result.typeDefinition,
                                 'level':result.level
                        }
                    returnList.append(listElement)
            return(returnList)
        else:   
            return(None)
    
    
    def checkDesc(self,parentKey=None,desc=None):
        if parentKey is not None and desc is not None:
            parentKey=ndb.Key(urlsafe=parentKey)
            query=ProductType().query(
                ProductType.typeDefinition==desc.upper(),
                                      ancestor=parentKey)
            if query.count()>0:
                print("checkDesc")
                print('true')
                return(True)
            else:
                print("checkDesc")
                print('false')
                return(False)

    def checkCode(self,parentKey=None,code=None):
        if parentKey is not None and code is not None:          
            parentKey=ndb.Key(urlsafe=parentKey)
            query=ProductType().query(
                  ProductType.typeCode==code.upper(),
                  ancestor=parentKey)
            if query.count()>0:
                return(True)
            else:
                return(False)

    
    def getTypeById(self,typeId=None):
        if typeId is not None:
            print(typeId)
            key=ndb.Key('ProductType',typeId)
            print(key)
            print(key.kind())
            print(key.id())
            print(key.urlsafe())
            print("trying to get entity")
            print(key.get())
            type=key.get()
            return(key.get())
        
    def getTypeByKey(self,key=None):
        if key is not None:
            return(key.get())
   
   
   
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

    
    
