from flask import Flask,request,abort
from flask import Response as flask_response,request
import json
import os,uuid
import datetime
from tableExtractor import extractTable
from buildModel import buildModelExcel,buildModelFromExcel
from predictDocument import classifyDocumentType

__name__='__main__'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\\uploads"
NB_Model = None

@app.route("/ping", methods=["GET"])
def ping():      
    response = {"response":"success"}     
    return flask_response(json.dumps(response),status=200,mimetype='application/json')


@app.route("/extract-tables", methods=["POST"])
def table_extraction():
   response = {"response":"success"} 
   file = request.files['file']    
   save_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
   print(save_path)
   file.save(save_path)   
   extractTable(save_path)
   return flask_response(json.dumps(response),status=200,mimetype='application/json')



@app.route("/buildModelExcel", methods=["GET"])
def buildExcelForModel():      
    response = {"response":"success"}  
    buildModelExcel()   
    return flask_response(json.dumps(response),status=200,mimetype='application/json')


@app.route("/buildModel", methods=["GET"])
def buildModel():
    response = {"response":"success"} 
    NB_Model,count_vectorizer = buildModelFromExcel()
    app.config['model'] = NB_Model
    app.config['countVectorizer'] = count_vectorizer
    print(NB_Model)
    return flask_response(json.dumps(response),status=200,mimetype='application/json') 


@app.route("/classify-document", methods=["POST"])
def classifyDocument():
   response = {"response":"success"} 
   file = request.files['file']    
   save_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
   print(save_path)
   file.save(save_path) 
   NB_Model = app.config['model'] 
   count_vectorizer = app.config['countVectorizer'] 
   if NB_Model is not None:
       print('Model loaded')
       documentType = classifyDocumentType(NB_Model,count_vectorizer,save_path)
       response =  documentType[0]
   else:
       print('Model not loaded')
   return flask_response(json.dumps(response),status=200,mimetype='application/json')



if __name__ == "__main__":
    app.run("0.0.0.0", port=9090,debug=True)

