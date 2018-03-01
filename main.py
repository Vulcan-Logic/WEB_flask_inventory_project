from flask import Flask,render_template,request,abort,make_response,redirect
from welcomeHandler import welcomeHandler
from productsHandler import addProduct
from productsHandler import listProductsHandler
from productsHandler import skuHandler
from typeHandler import catType
import logging
import json
from mainSub import *



app = Flask(__name__)

@app.route('/')
def index():
    return(render_template("welcome.html"))

@app.route('/products/<string:productPage>',methods=['GET', 'POST'])
def products(productPage):
    try:
        if productPage=="add":
            if request.method=='GET':
            #get results from logic layer
                sData=addProduct().get()
            #prepare response
                if sData is not None:
                    return(render_template("ap.html",sData=sData,cont=True))
                else:
                    return(render_template("ap.html",cont=False))
            elif request.method=='POST':
                if gcsFunction2(request):
                    return(redirect("/products/add",code=303))
                else:
                    raise Exception(500,"Server Error")
        elif productPage=="rqst":
            rqstType=request.args.get("type")
            fileName=request.args.get("name")
            data=request.data
            if rqstType=="storageTest":
                gcsFunction1(fileName,data)
                response=make_response("OK") 
                #response.headers['Content-Type'] = 'text/json'
                response.status_code = 200
                return(response)
            elif rqstType=="chkSt":
                print("in chkst")
                print(request.form)
                return("OK")
        elif productPage=="list":
            return("listHandler")
        elif productPage=="sku":
            return("skuHandler")
        else:
            abort(404)
    except Exception as e:
        x,y = e.args
        if x==500:
            abort(500)
        elif x==404:
            abort(404)
        else:
            server_error(e)

    
@app.route('/types/<string:typePage>',methods=['GET','POST'])
def types(typePage):
    catT=catType()
    try:
        if typePage=="checkDesc":
            #get request arguments
            parentId=request.args.get("parentId")
            desc=request.args.get("Desc")
            #get results from logic layer
            if catT.checkDesc(parentId,desc):
                retValue=json.dumps({"response":"true"})
            else:
                retValue=json.dumps({"response":"false"})
            #prepare response
            response=make_response(retValue) 
            response.headers['Content-Type'] = 'text/json'
            response.status_code = 200
            return(response)
        elif typePage=="checkCode":
            #get request arguments
            parentId=request.args.get("parentId")
            desc=request.args.get("Code")
            #get results from logic layer
            if catT.checkCode(parentId,desc):
                retValue=json.dumps({"response":"true"})
            else:
                retValue=json.dumps({"response":"false"})
            #prepare response
            response=make_response(retValue) 
            response.headers['Content-Type'] = 'text/json'
            response.status_code = 200
            return(response)
        elif typePage=="insertType":
            if request.method=="POST":
                #get request arguments
                parentKey=request.args.get("parentId")
                typeDesc=request.args.get("Desc")
                typeCode=request.args.get("Code")
                #get results from logic layer
                retList=catT.put(parentKey,typeDesc,typeCode)
                #prepare response
                if retList is not None:
                    response=make_response(retList)
                    response.headers['Content-Type']='text/json'
                    response.status_code = 200
                else:
                #error - no results from logic layer
                    raise Exception(500,"Server Error")
                return(response)
            else:
                raise Exception(404,"Page Not Found")
        elif typePage=="getTypeList":
            #get request arguments
            keyUrl=request.args.get('kId')
            #get results from logic layer
            retList=catT.getChildList(keyUrl)
            #prepare response            
            if retList is not None:
                response=make_response(retList)
                response.headers['Content-Type'] = 'text/json'
                response.status_code = 200
            else:
            #error - no results from logic layer
                raise Exception(500,"Server Error")
            return(response)
        else:
        #error page not found
            raise Exception(404,"Page Not found")
    except Exception as e:
        x,y = e.args
        if x==500:
            abort(500)
        elif x==404:
            abort(404)
        else:
            server_error(e)
        
@app.errorhandler(500)
def error500(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

@app.errorhandler(404)
def error404(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 404

def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

#app = (webapp2.WSGIApplication([('/', welcomeHandler),
#                                 ('/addInitialTypes',initialAddtype),
#                                 ('/products/getTypeList',getTypeList),
#                                 ('/products/add',addProductsHandler),
#                                 ('/products/list',listProductsHandler),
#                                 ('/products/sku',skuHandler),
#                                 ('/products/checkDesc',validateTypeDesc),
#                                 ('/products/checkCode',validateTypeCode),
#                                 ('/products/insertType',insertType),
#                                 ('/starterTest', getStarterTypes),
#                                 ('/getStarterTypesJSON', 
#                                                     getStarterTypesJSON)], 
#                                debug = True))



