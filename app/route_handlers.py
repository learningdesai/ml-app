from app import app
import os
from flask import request, redirect, jsonify
from werkzeug.utils import secure_filename

from app.core.Predictor import Predictor
from app.core.PredictorSingle import PredictorSingle
from app.core.Train import Train
from app.core.ShipmentGraph import ShipmentGraph as Graph

from app.config import *
from app.route_utils import *

import logging
import json

logging.basicConfig(filename='log_data.log',level=logging.DEBUG)


def get_test_summary(is_metrics=False):    
    filename = request.args.get('file')
    filename = handle_missing_test_file(filename)        
    
    mode = request.args.get('mode')
    mode = handle_missing_mode(mode)
    
    try:
        filename = DATASETS_FOLDER + filename + ".csv"
        #cols, encoder_data, env = get_para(mode=mode)  
        
        pd = Predictor(filename, mode=mode)
        print("predictor called")
        results = pd.start(metrics=True, mode=mode)        
        print("predicted and results")
        results["status"] = "success"
    except Exception as e:                
        logging.warning(str(e))
        results = {
            "status": "failure", 
            "error": "route_handlers:get_test_summary::check your url or  data format"
        }
    
    if results["status"] == "success":
        if is_metrics:
            results = results["metrics"]
        else:
            results = results["json_result"]
    return jsonify(results)

def get_test_summary_single():
    json_data = request.get_json(force=True)
    print(type(json_data))
    try:
        pd = PredictorSingle(json_data)
        print("predictor loaded. calling start..")
        results = pd.start()
        print("predicted and results")
        results["status"] = "success"
    except Exception as e:
        logging.warning(str(e))
        results = {
            "status": "failure", 
            "error": "route_handlers:get_test_summary_single::check your url or  data format"
        }
    if results["status"] == "success":        
            results = results["json_result"]
    return jsonify(results)
        

def generate_model():
    filename = request.args.get('file')
    filename = handle_missing_test_file(filename)        
    
    mode = request.args.get('mode')
    mode = handle_missing_mode(mode)
    try:
        filename = DATASETS_FOLDER + filename + ".csv" 
        if mode == None:
            mode = ""
        #cols, encoder_data, env = get_para(mode=mode)        
        t = Train(mode=mode, TRAIN_FILE=filename)
        rsq = t.train()
        result = { "status": "success", "message": "model generated", "r_sq": rsq }
    except Exception as e:
        logging.warning(str(e))
        result = { "status": "failure", 
                  "error": "route_handlers:generate_model::Data format is not as expected" }
    
    return jsonify(result)
    
def get_test_plots(mode=None):    
    # exception is handled in root file - Graph
    filename = request.args.get('file')
    filename = handle_missing_test_file(filename)
    try:
        filename = DATASETS_FOLDER + filename + ".csv"
        #cols, encoder_data, env = get_para(mode=mode)  
        print(filename)          
        pd = Predictor(filename, mode=mode)
        results = pd.start(mode=mode)
        json_results = results["json_result"]    
        g = Graph()
        results = g.start(json_results)
    except Exception as e:
        logging.warning(str(e))
        results = {
            "status": "failure", 
            "error": "route_handlers:get_test_plots::check your url or  data format"
        }
    return jsonify(results)

def get_demo_urls():
    results =  {
            "sample_summary_url": DOMAIN + "/summary?file=" + DEFAULT_TEST_FILE,
            "sample_metrics_url": DOMAIN + "/metrics?file="+DEFAULT_TEST_FILE,
            "sample_month_summary": DOMAIN + "/summary?file=" + DEFAULT_TEST_FILE +"_m&mode=month",
            "sample_month_metrics": DOMAIN + "/metrics?file=" + DEFAULT_TEST_FILE +"_m&mode=month",
            "sample_weight_summary": DOMAIN + "/summary?file=" + DEFAULT_TEST_FILE +"_w&mode=weight",
            "sample_weight_metrics": DOMAIN + "/metrics?file=" + DEFAULT_TEST_FILE +"_w&mode=weight",
            "sample_model_generate": DOMAIN + "/model_generate?file=" + DEFAULT_TEST_FILE,
            "sample_month_plot": DOMAIN + "/plot?file=" + DEFAULT_TEST_FILE,
        }
    return jsonify(results)

def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:           
        print('no file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        print('no selected file part')
        return redirect(request.url)
    if file and allowed_file(file.filename) and (not does_file_exist(file.filename)):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        results = {"status": "success"}        
    else:
        results = {"status": "failure", "error": "file exists OR invalid file"}
    return jsonify(results)

def update_config():
    json_data = request.get_json(force=True)
    try:
        filepath = CONFIG_FOLDER + json_data["filename"] + ".json"
        with open(filepath, "w") as jsonFile:
            data = {
                "cols": json_data["cols"],
                "encoder_data": json_data["encoder_data"]
            }
            json.dump(data, jsonFile)
        return jsonify({"status": "success"})
    except Exception as e:
        logging.warning(str(e))
    return jsonify({"status": "failur", "error": "check log details"})

"""
# EXAMPLE POST DATA TO BE SENT FOR UPDATE_CONFIG
{
	"filename": "month",
	"cols": {
		"f_cols": ["ShipmentCount", "MonthNumber"],
		"conditions": {			
			"ShipmentCount": ["lt", 20]
		},
		"agg_cols": []

	},
	"encoder_data": {
				
	}
}
"""