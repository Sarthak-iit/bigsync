from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse  # Ensure JSONResponse is imported
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import Query
import numpy as np 
import traceback
import os
import pandas as pd
from typing import List, Dict

import json
from algos.event_detection import eventDetection
from algos.event_classification import eventClassification
from algos.event_classification_islanding import classifyIslandingEvent
from algos.baselining import findStats
from algos.Algorithms.EWT.EWT_Main import EWTmainFunction
from typing import List
from algos.Algorithms.window_selection import windowSelection
from algos.Algorithms.Prony.prony3 import pronyAnalysis
from algos.Algorithms.OSLP.main import oslp_main
from gsfl.gsfl_algorithm import perform_gauss_seidel,calculate_Y_bus
from gsfl.contingency_analysis import calculate_losf, calculate_gosf, calculate_base_flows
from gsfl.nrlf_algorithm import perform_newton_raphson
from gsfl.fdlf_algorithm import perform_fdlf

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class EventDetectionSettings(BaseModel):
    time : List[float]
    windowSize: float = None
    sd_th: float = None
    data: List[float]

class EventClassificationSettings(BaseModel):
    time: List[float]
    data: List[float]
    thresholdValues: Dict[str, float]
    
class IslandingEventClassificationSettings(BaseModel):
    time: List[float]
    data: List[List[float]]
    thresholdValues: dict

class StatisticsSettings(BaseModel):
    data: List[float]

class ModeAnalysisSettings(BaseModel):
    data: List[float]

class OSLPSettings(BaseModel):
    time : List[float]
    data: Dict[str, Dict[str, List[float]]] = {
    "Sub1-l1": {
        'F': [0.0] * 5000,
        'V': [0.0] * 5000,
        'VA': [0.0] * 5000,
        'I': [0.0] * 5000,
        'IA': [0.0] * 5000
    }
}
    points:List[float]

@app.post("/v2/gslf")
async def gslf(
    file: UploadFile = File(...),
    acceleration_factor: float = Form(...),
):
    print(f"Received file: {file.filename}")
    print(f"Received acceleration factor: {acceleration_factor}")   
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the contents of the file
        contents = await file.read()
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create temp directory if not exists
        with open(file_location, "wb") as f:
            f.write(contents)

        # Read the Excel file into DataFrames
        Edata = pd.read_excel(file_location, sheet_name=0).to_numpy()  # Reading elements data
        Ndata = pd.read_excel(file_location, sheet_name=1).to_numpy()  # Reading nodes power data
        
        # Call your calculation function (ensure it returns correctly)
        print("clear")
        result = perform_gauss_seidel(Edata, Ndata, acceleration_factor)
        print(result)

        if 'final_voltages' in result:
            # Convert the complex numbers in final_voltages
            final_voltages = result['final_voltages']
            result['final_voltages'] = final_voltages


        # Clean up: remove the temporary file after processing
        os.remove(file_location)
        print(result)
        return JSONResponse(content={"result": result})

    except Exception as e:
        print("exception")
        return JSONResponse(content={"error": str(e)}, status_code=400)
    
@app.post("/v2/nrlf")
async def nrlf(
    file: UploadFile = File(...),
    tolerance: float = Form(...),
    max_iterations: float = Form(...),
):
    print(f"Received file: {file.filename}")
    print(f"Received tolerance: {tolerance}")
    print(f"Received max_iterations: {max_iterations}")
       
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the contents of the file
        contents = await file.read()
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create temp directory if not exists
        with open(file_location, "wb") as f:
            f.write(contents)

        # Read the Excel file into DataFrames
        Edata = pd.read_excel(file_location, sheet_name=0).to_numpy()  # Reading elements data
        Ndata = pd.read_excel(file_location, sheet_name=1).to_numpy()  # Reading nodes power data
        
        # Call your calculation function (ensure it returns correctly)
        result = perform_newton_raphson(Edata, Ndata,tolerance,max_iterations)
        print(result)

        if 'final_voltages' in result:
            # Convert the complex numbers in final_voltages
            final_voltages = result['final_voltages']
            result['final_voltages'] = final_voltages


        # Clean up: remove the temporary file after processing
        os.remove(file_location)
        print(result)
        return JSONResponse(content={"result": result})

    except Exception as e:
        print(traceback.format_exc())
        print("exception")
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/v2/fdlf")
async def fdlf(
    file: UploadFile = File(...),
    tolerance: float = Form(...),
    max_iterations: float = Form(...),
):
    print(f"Received file: {file.filename}")
    print(f"Received tolerance: {tolerance}")
    print(f"Received max_iterations: {max_iterations}")
       
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the contents of the file
        contents = await file.read()
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create temp directory if not exists
        with open(file_location, "wb") as f:
            f.write(contents)

        # Read the Excel file into DataFrames
        Edata = pd.read_excel(file_location, sheet_name=0).to_numpy()  # Reading elements data
        Ndata = pd.read_excel(file_location, sheet_name=1).to_numpy()  # Reading nodes power data
        
        # Call your calculation function (ensure it returns correctly)
        result = perform_fdlf(Edata, Ndata,tolerance,max_iterations)
        print(result)

        if 'final_voltages' in result:
            # Convert the complex numbers in final_voltages
            final_voltages = result['final_voltages']
            result['final_voltages'] = final_voltages


        # Clean up: remove the temporary file after processing
        os.remove(file_location)
        print(result)
        return JSONResponse(content={"result": result})

    except Exception as e:
        print(traceback.format_exc())
        print("exception")
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/v2/losf")
async def losf_endpoint(
    file: UploadFile = File(...),
    outageLine: float = Form(...),
    ):
    try:
        # Read the uploaded file
        print("Losf Started")
        contents = await file.read()
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create temp directory if not exists
        with open(file_location, "wb") as f:
            f.write(contents)

        # Read the Excel file into DataFrames
        Edata = pd.read_excel(file_location, sheet_name=0).to_numpy()  # Line data
        Ndata = pd.read_excel(file_location, sheet_name=1).to_numpy()  # Bus data
        Ybus = calculate_Y_bus(Edata)
        print("Ybus")
        base_flows = calculate_base_flows(Ndata,Edata)

        # Calculate LOSF
        losf_results = calculate_losf(Ybus, Edata, base_flows, outageLine)
        print("losf_results")

        os.remove(file_location)  # Clean up
        return JSONResponse(content={"losf_results": losf_results})
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=400)

@app.post("/v2/gosf")
async def gosf_endpoint(file: UploadFile = File(...),
    outageGen: float = Form(...),
    ):
    try:
        # Read the uploaded file
        contents = await file.read()
        file_location = f"temp/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)  # Create temp directory if not exists
        with open(file_location, "wb") as f:
            f.write(contents)

        # Read the Excel file into DataFrames
        Edata = pd.read_excel(file_location, sheet_name=0).to_numpy()  # Line data
        Ndata = pd.read_excel(file_location, sheet_name=1).to_numpy()  # Line data

        Ybus = calculate_Y_bus(Edata)
        
        base_flows = calculate_base_flows(Ndata,Edata)

        # Calculate GOSF
        gosf_results = calculate_gosf(Ybus, Edata, base_flows, outageGen)

        os.remove(file_location)  # Clean up
        return JSONResponse(content={"gosf_results": gosf_results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@app.get("/")
def index():
    return {"message": "Welcome to the API"}


@app.post("/v2/classify-event")
async def classify_event_data(event_settings: EventClassificationSettings):
    if not event_settings.time or not event_settings.data or not event_settings.thresholdValues:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    res = eventClassification(
        event_settings.data, event_settings.time,
        event_settings.thresholdValues,
    )
    return res

@app.post("/v2/detect-event")
async def detect_event(event_settings: EventDetectionSettings):
    if not event_settings.time or not event_settings.data:
        raise HTTPException(status_code=400, detail="Bad request from the client")

    res = eventDetection(
        event_settings.data, event_settings.time,
        float(event_settings.windowSize),
        float(event_settings.sd_th),
    )
    if res and res["fault"]:
        return res
    return {"fault": False}

@app.post("/v2/detect-islanding-event")
async def detect_islanding_event(event_settings: IslandingEventClassificationSettings):
    if not event_settings.time or not event_settings.data or not event_settings.thresholdValues:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    res = classifyIslandingEvent(
        event_settings.data, event_settings.time,
        event_settings.thresholdValues,
    )
    return res

@app.post("/v2/find-statistics")
async def detect_islanding_event(event_settings: StatisticsSettings):
    if not event_settings.data:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    
    res = findStats(
        event_settings.data
    )
    return res

@app.post("/v3/modes-analysis")
async def mode_analysis(event_settings: ModeAnalysisSettings):
    if not event_settings.data:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    modes_data =  EWTmainFunction(event_settings.data)
    ewt_data = modes_data["ewt"]
    prony_data = []
    for i in range(len(modes_data["Amp"])):
        selected_window = windowSelection(ewt_data[i], modes_data["InstEner"][i], modes_data["InstFreq"][i])
        if len(selected_window) > 0:
            x = pronyAnalysis(selected_window)
            prony_data.append(x+[modes_data["PerEner"][i]])
        else:
            prony_data.append(None)
    filtered_modes_data = {
    "ewt": [],
    "Amp": [],
    "InstEner": [],
    "InstFreq": []
    }

    for i, item in enumerate(prony_data):
        if item is not None:
            filtered_modes_data["ewt"].append(modes_data["ewt"][i])
            filtered_modes_data["Amp"].append(modes_data["Amp"][i])
            filtered_modes_data["InstEner"].append(modes_data["InstEner"][i])
            filtered_modes_data["InstFreq"].append(modes_data["InstFreq"][i])
    filtered_modes_data["ewt"] = np.array(filtered_modes_data["ewt"])
    filtered_modes_data["Amp"] = np.array(filtered_modes_data["Amp"])
    filtered_modes_data["InstEner"] = np.array(filtered_modes_data["InstEner"])
    filtered_modes_data["InstFreq"] = np.array(filtered_modes_data["InstFreq"])
    prony_data = [x for x in prony_data if x is not None]
    
    return json.dumps({'Mode':filtered_modes_data["ewt"].tolist(),'Amp':filtered_modes_data["Amp"].tolist(),'InstEner':filtered_modes_data["InstEner"].tolist(),'InstFreq':filtered_modes_data["InstFreq"].tolist(), 'Prony_data':prony_data })

@app.post("/v2/oslp")
async def oslp_analysis(event_settings: OSLPSettings):
    if not event_settings.data or not event_settings.points:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    res = oslp_main(event_settings.time,event_settings.data, event_settings.points[0], event_settings.points[1])
    # res = findStats(
    #     event_settings.data
    # )
    return res


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return {"error": "An unexpected error occurred"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return {"error": "Validation error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
