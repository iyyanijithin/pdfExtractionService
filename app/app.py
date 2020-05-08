from flask import Flask,request,abort
from flask import Response as flask_response,request
import json
import os,uuid
import datetime
from tableExtractor import extractTable

__name__='__main__'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\\uploads"


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




if __name__ == "__main__":
    app.run("0.0.0.0", port=9090,debug=True)
