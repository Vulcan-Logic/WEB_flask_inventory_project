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
    typeImageLoc=ndb.StringProperty()
    level=ndb.IntegerProperty()
    counter=ndb.IntegerProperty()
    dateModified=ndb.DateTimeProperty(auto_now=True)
    modifiedBy=ndb.KeyProperty()

#this should be associated 
#with the category and not individual products
class ProductTypeFixedAttributes(ndb.Model):
    attrName=ndb.StringProperty()
    attrType=ndb.StringProperty()
    attrReqd=ndb.BooleanProperty()
    attrMinLen=ndb.IntegerProperty()
    attrMaxLen=ndb.IntegerProperty()

class ProductTypeAttribQuery():
    #need to pass parent category key to get attributes for this category
    def get(self,parentKey=None):
        if parentKey is not None:
            if parentKey=="0":
                parentKey=ndb.Key('ProductType',"0")
            else:
                parentKey=ndb.Key(urlsafe=parentKey)
        attrQuery=ProductTypeFixedAttributes.query(parent=parentKey)
        returnList=[]
        if attrQuery.count()>0:
            results=attrQuery.fetch()
            for result in results:
                listElement={ 
                    'attrName': result.attrName,
                    'required': result.attrReqd,
                    'mnLen':result.attrMinLen,
                    'mxLen':result.attrMaxLen
                     }
                returnList.append(listElement)
            return(returnList)
        else:
            return(None)
    #set attributes for this category of products    

    def set(self,default=True,attribList=None,parentkey=None):
        pass

    
class TypeQuery():
    
    def addType(self,typeCode,typeDefinition,typeImageLoc,parentKey=None):
        #to do 
        # make sure that the default attributes for this type are carried 
        #on from parent to child 
        if parentKey is not None:
            if parentKey=="0":
                parentKey=ndb.Key('ProductType',"0")
            else:
                parentKey=ndb.Key(urlsafe=parentKey)
            parentType=self.getTypeByKey(parentKey)
            if parentType is not None:
                typeEntry=ProductType(typeCode = typeCode.upper(), 
                                    counter = 0,
                                    level = parentType.level+1, 
                                    typeDefinition = typeDefinition.upper(),
                                    typeImageLoc=typeImageLoc,
                                    parent = parentKey)
                returnKey = typeEntry.put()
            else: 
                return(None)
        else:
            parentKey=ndb.Key('ProductType',"0")      
            typeEntry=ProductType(typeCode = typeCode.upper(), 
                                counter = 0, 
                                level=0,
                                typeDefinition = typeDefinition.upper(),
                                typeImageLoc=typeImageLoc,
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
                    if parentKey.urlsafe()!=result.key.urlsafe():
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
            if parentKey=="0":
                parentKey=ndb.Key('ProductType',"0")
                checkLevel=0
            else:
                parentKey=ndb.Key(urlsafe=parentKey)
                parentType=self.getTypeByKey(parentKey)
                checkLevel=parentType.level+1
            print("checking description")
            print("description is")
            print(desc)
            query=ProductType().query(
                ProductType.typeDefinition==desc.upper(),
                ProductType.level==checkLevel,
                                      ancestor=parentKey)
            print("query is")
            print(query)
            if query.count()>0:
                print("check Desc")
                print("returned False")
                return(False)
            else:
                return(True)
        else:
            return(False)

    def checkCode(self,parentKey=None,code=None):
        if parentKey is not None and code is not None:  
            if parentKey=="0":
                parentKey=ndb.Key('ProductType',"0")
                checkLevel=0
            else:
                parentKey=ndb.Key(urlsafe=parentKey)        
                parentType=self.getTypeByKey(parentKey)
                checkLevel=parentType.level+1
            query=ProductType().query(
                  ProductType.typeCode==code.upper(),
                  ProductType.level==checkLevel,
                  ancestor=parentKey)
            print("query is")
            print(query)
            print("result count")
            print(query.count())
            if query.count()>0:
                print("check Code")
                print("returned False")
                return(False)
            else:
                return(True)

    
    def getTypeByKey(self,key=None):
        if key is not None:
            return(key.get())
        
    def getCounterByKey(self,key=None):
        if key is not None:
            key=ndb.Key(urlsafe=key)
            tType=key.get()
            if tType:
                return(tType.counter)
            else:
                err="Server Error:unable to get counter from DB"
                raise Exception("500",err)
        else: 
            raise Exception("500","Server Error: Invalid Key for get counter")

    def setTypeCounterByKey(self,key=None):
        if key is not None:
            key=ndb.Key(urlsafe=key)
            tType=key.get()
            counter=tType.counter+1
            tType(counter=counter)
            tType.put()
            return(counter)
        else:
            raise Exception("500", \
            "Server Error: Invalid Key for set counter")

    def getChildTypesByKey(self,key=None):
        #key in url safe mode, level int 
        if key is not None and key!="0": 
                parentKey=ndb.Key(urlsafe=key)
                typ=self.getTypeByKey(parentKey)
                level=typ.level+1
        else:
            parentKey=ndb.Key('ProductType',"0")
            level=0
        query=ProductType().query(ProductType.level==level, 
                                  ancestor=parentKey).order(
                                               ProductType.dateModified)    
        returnList=[]
        if query.count()>0:
            results=query.fetch()
            for result in results:
                if parentKey.urlsafe()!=result.key.urlsafe():
                    listElement={ 
                                'key': result.key.urlsafe(),
                                'typeCode': result.typeCode,
                                'typeDefinition':result.typeDefinition,
                                'level':result.level
                    }
                returnList.append(listElement)
        return(returnList)
                 
   
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

    
    
