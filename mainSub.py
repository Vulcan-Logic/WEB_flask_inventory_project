from google.appengine.api import app_identity
from werkzeug.utils import secure_filename
import cloudstorage as gcs
import mimetypes
import base64
import os
import logging
import datetime
from productsHandler import addProduct
from typeHandler import catType


def gcsFunction1(fileName=None,data=None):
#using an ordinary post request with file as the data stream
    my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
    gcs.set_default_retry_params(my_default_retry_params)
    bucket_name = os.environ.get('BUCKET_NAME',
                       app_identity.get_default_gcs_bucket_name())
    bucket = '/' + bucket_name
    filename = bucket + '/'+fileName
    content_t=mimetypes.guess_type(data)
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    try:
        gcs_file = gcs.open(filename,
                    'w',
                    content_type=content_t,
                    options={'x-goog-meta-filename': fileName},
                    retry_params=write_retry_params)
        #get only the data stream
        data=data.split(',')[1]
        #convert data to proper binary format for saving
        data=base64.b64decode(data)
        gcs_file.write(data)
        gcs_file.close()
    except Exception as e:
        logging.exception(e)
        raise Exception(500,"Server Error:" + e) 
    return(True)

def gcsFunction2(request):
    #forgot the type parent key?-------
    pKey=request.form.get("pKey")
    pName=request.form.get("pName")
    pSku=request.form.get("pSku")
    prodDesc=request.form.get("prodDesc")
    noAttr=request.form.get("noAttr")
    #change this to user id
    modifiedBy=None  
    pFieldList=[]
    pImageList=[]
    #set images list 
    for tFile in request.files:
        fileCont=request.files[tFile]
        if fileCont.filename!='':
            try:
                filename,fileName=gcsWrite(fileCont,pSku)
            except Exception as e:
                logging.exception(e)
                raise Exception(500, str(e))
            if filename is not None: 
                pImageEnt={"imageName":fileName,"imageLocation":filename}
                pImageList.append(pImageEnt)
    #set attributed repeated fields list    
    noAttr=int(noAttr)
    for ctr in range(1,noAttr+1):
        attrDesc=str(ctr)+"attrDesc"
        attrValue=str(ctr)+"attrValue"
        attrDescVal=request.form.get(attrDesc)
        attrValueVal=request.form.get(attrValue)
        pFieldEnt={"fieldName":attrDescVal,"fieldValue":attrValueVal}
        pFieldList.append(pFieldEnt)
    # try to insert    
    try:
        addProduct().put(pKey=pKey,
                        pName=pName,
                        pSku=pSku, 
                        prodDesc=prodDesc,
                        pFieldList=pFieldList,
                        pImageList=pImageList, 
                        modifiedBy=modifiedBy)
    except Exception as e:
        logging.exception(e)
        raise Exception(500,str(e)) 
        
def gcsWrite(cont,iden,cType="file",fileName=None):
    #set storage parameters and options
    my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
    gcs.set_default_retry_params(my_default_retry_params)
    #get the right storage folder 
    bucket_name = os.environ.get('BUCKET_NAME',
                       app_identity.get_default_gcs_bucket_name())
    bucket = '/' + bucket_name
    #get the time for including in filename for uniqueness
    now=datetime.datetime.now()
    #check content type: file or data and set the right parameters    
    if cType=="file":
        content_t=cont.mimetype
        #secure filename
        fileName=cont.filename
    else:
        #try to guess the data type based on data stream content
        content_t=mimetypes.guess_type(cont)
        #get only the data stream
        cont=cont.split(',')[1]
        #decode the data into proper format for image file
        cont=base64.b64decode(cont)
    #build the right filenames for storage to file system
    fileName=secure_filename(fileName)
    fileName1=iden+now.isoformat()+fileName
    filename = bucket + '/'+fileName1
    #re-set storage write parameters     
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    #try to write data to storage
    try:
        #open gcs file
        gcs_file = gcs.open(filename,
                    'w',
                    content_type=content_t,
                    options={'x-goog-meta-filename': fileName},
                    retry_params=write_retry_params)
        #check content type: file or data
        if cType=="file":
            #get file contents as data stream
            gcs_file.write(cont.stream.read())
        else:
            #data is already in the right format
            gcs_file.write(cont)
        #close gcs file   
        gcs_file.close()
    except Exception as e:
        logging.exception(e)
        raise Exception(500,str(e)) 
    return(filename,fileName)
    
def gcsFunction3(request):
    parentKey=request.args.get("parentId")
    typeDesc=request.args.get("Desc")
    typeCode=request.args.get("Code")
    typeImage=request.args.get("filename")
    data=request.data
    iden=typeCode
    try:
        if typeImage is not None and typeImage!="null" :
            filename,_=gcsWrite(data,iden,cType="data",
                                       fileName=typeImage)
            retList=catType().put(parentKey=parentKey,
                                  typeDesc=typeDesc,
                                  typeCode=typeCode,
                                  filename=filename)
        else:
            retList=catType().put(parentKey=parentKey,
                                  typeDesc=typeDesc,
                                  typeCode=typeCode)
        return(retList)
    except Exception as e:
        logging.exception(e)
        raise Exception(500,str(e)) 
    
    
def getTypes(type=None,level=None,key=None):
    pass

def getProduct(key=None, parentKey=None):
    pass

    
        