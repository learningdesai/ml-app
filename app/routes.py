from app import app
from flask import Flask, request, jsonify
from app.config import UPLOAD_FOLDER
from app.route_handlers import *


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index')
def index():    
    return get_demo_urls()


@app.route('/summary', methods=['GET'])
def get_summary():        
    return get_test_summary()

@app.route('/summary_single', methods=['POST'])
def get_summary_single():        
    return get_test_summary_single()
        
@app.route('/metrics', methods=['GET'])
def get_metrics():    
    return get_test_summary(is_metrics=True)


@app.route('/model_generate', methods=['GET'])
def generate_models():        
    return generate_model()
   

@app.route('/upload', methods=['POST', 'GET'])
def upload_data_file():
    upload_file()


@app.route('/plot', methods=['GET'])
def plot_results():    
    return get_test_plots()

@app.route('/update_config', methods=['POST'])
def config_update():    
    return update_config()








    