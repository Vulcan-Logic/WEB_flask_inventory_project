from google.appengine.api import app_identity
from werkzeug.utils import secure_filename
import cloudstorage as gcs
import mimetypes
import base64
import os
import logging
import datetime
from productsHandler import addProduct


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
    print(content_t)
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
        raise Exception(500,"Server Error") 
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
    if len(request.files>0):
        for tFile in request.files:
            fileCont=request.files[tFile]
            filename,fileName=gcsWrite(fileCont,pSku)
            if filename is not None: 
                pImageEnt={"imageName":fileName,"fileLocation":filename}
                pImageList.append(pImageEnt)
    else:
        pImageList=None
    noAttr=int(noAttr)
    for ctr in range(1,noAttr+1):
        attrDesc=str(ctr)+"attrDesc"
        attrValue=str(ctr)+"attrValue"
        attrDescVal=request.form.get(attrDesc)
        attrValueVal=request.form.get(attrValue)
        pFieldEnt={"fieldName":attrDescVal,"fieldValue":attrValueVal}
        pFieldList.append(pFieldEnt)
    try:
        addProduct.put(pKey,pName,pSku,prodDesc,pFieldList, 
        pImageList, modifiedBy)
    except Exception as e:
        logging.exception(e)
        raise 
        
def gcsWrite(fileCont,pSku):
    my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
    gcs.set_default_retry_params(my_default_retry_params)
    bucket_name = os.environ.get('BUCKET_NAME',
                       app_identity.get_default_gcs_bucket_name())
    bucket = '/' + bucket_name
    now=datetime.datetime.now()
    fileName=secure_filename(fileCont.filename)
    fileName1=pSku+now.isoformat()+fileName
    filename = bucket + '/'+fileName1
    content_t=fileCont.mimetype
    write_retry_params = gcs.RetryParams(backoff_factor=1.1)
    try:
        gcs_file = gcs.open(filename,
                    'w',
                    content_type=content_t,
                    options={'x-goog-meta-filename': fileName},
                    retry_params=write_retry_params)
        gcs_file.write(fileCont.stream.read())
        gcs_file.close()
    except Exception as e:
        logging.exception(e)
        raise Exception(500,"Server Error") 
    return(filename,fileName)
    
    
    
    
        