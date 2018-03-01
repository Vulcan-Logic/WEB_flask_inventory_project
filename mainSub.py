from google.appengine.api import app_identity
from werkzeug.utils import secure_filename
import cloudstorage as gcs
import mimetypes
import base64
import os
import logging


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
    pName=request.form.get("pName")
    pSku=request.form.get("pSku")
    prodDesc=request.form.get("prodDesc")
    prodImageDesc=request.form.get("prodImageDesc")
    noAttr=request.form.get("noAttr")
    for file in request.files:
        fileCont=request.files[file]
        gcsWrite(fileCont)
    noAttr=int(noAttr)
    for ctr in range(1,noAttr+1):
        attrDesc=str(ctr)+"attrDesc"
        attrValue=str(ctr)+"attrValue"
        attrDescVal=request.form.get(attrDesc)
        attrValueVal=request.form.get(attrValue)
# save all attributes in datastore
    return(True)
        
def gcsWrite(fileCont):
    my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
    gcs.set_default_retry_params(my_default_retry_params)
    bucket_name = os.environ.get('BUCKET_NAME',
                       app_identity.get_default_gcs_bucket_name())
    bucket = '/' + bucket_name
    fileName=secure_filename(fileCont.filename)
    filename = bucket + '/'+fileName
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
    return(True)
    
    
    
    
        