from flask import Flask, request, render_template
from flask_cors import CORS
import pandas as pd
from algorithms.main import FaultDetection 
from algorithms.main import EventClassification
import json

app = Flask(__name__)
# Allow requests from all origins
CORS(app)

# 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file found"
    file = request.files['file']
    windowSize = float(request.form['windowSize']) if 'windowSize' in request.form else None
    sd_th = float(request.form['sd_th']) if 'sd_th' in request.form else None
    print(request.form)
    if file.filename == '':
        return "No selected file"
    if file:
        faultDetection = FaultDetection()
        res = faultDetection.getFault(file,windowSize,sd_th)
        # res = algorithm(file,windowSize,0.025)
        if(res):
            data_freq = res[0].tolist()
            data_rocof = res[1].tolist()
            # data_sd_rocof = res[2].tolist()
            # data_sd_rocof = data_sd_rocof + [0] * (len(data_freq) - len(data_sd_rocof))
            data_time = res[2].tolist()
            return {"fault":True,"freq":data_freq, "time":data_time,"rocof":data_rocof}
        else:
            return {"fault":False}
@app.route('/classifyEvent',methods=['POST'])
def classifyEvent():
    if 'file' not in request.files:
        return "No file found"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        eventClasify =  EventClassification(file)
        return eventClasify.classifyEvents()



if __name__ == '__main__':
    app.run(port=5000)
