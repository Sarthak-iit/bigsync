from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from fastapi import HTTPException
import io
from fastapi.responses import JSONResponse

import numpy as np 
from typing import List, Dict

import json
import pandas as pd
from io import BytesIO
from algos.event_detection import eventDetection
from algos.event_classification import eventClassification
from algos.event_classification_islanding import classifyIslandingEvent
from algos.baselining import findStats
from algos.Algorithms.EWT.EWT_Main import EWTmainFunction
from typing import List
from algos.Algorithms.window_selection import windowSelection
from algos.Algorithms.Prony.prony3 import pronyAnalysis
from algos.Algorithms.OSLP.main import oslp_main
from algos.faultClassificationSC import faultClassificationSequenceComponents
from algos.faultDetectionSample import faultClassificationSampleToSample
from algos.faultDetectionCycle import faultClassificationCycleToCycle
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


@app.post("/v2/FCSQ")
async def FCSQ(file: UploadFile = File(...), totalTime: float = Form(...), faultTimeInstant: float = Form(...), faultDuration: float = Form(...)):
    try:
        import openpyxl
        file_content = await file.read()
        excel_data = pd.read_excel(io.BytesIO(file_content), engine="openpyxl")
        
        response_data = faultClassificationSequenceComponents(
            excel_data, totalTime, faultTimeInstant, faultDuration
        )
        return JSONResponse(content=response_data)
    except ImportError:
        raise HTTPException(status_code=500, detail="Missing required dependency: openpyxl. Install it using `pip install openpyxl`.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/v2/FD")
async def FD(file: UploadFile = File(...), samplingRate: float = Form(...), threshold: float = Form(...), analysisTypeValue: float = Form(...)):
    try:
        # Read Excel file
        import openpyxl
        file_content = await file.read()
        excel_data = pd.read_excel(io.BytesIO(file_content), engine="openpyxl")

        # Call the appropriate function based on analysisTypeValue
        if analysisTypeValue == 0.0:
            mn_time, mx_time = faultClassificationSampleToSample(excel_data, threshold)
        elif analysisTypeValue == 1.0:
            mn_time, mx_time = faultClassificationCycleToCycle(excel_data, threshold, samplingRate)

        # Return JSON response
        if mn_time is not None and mx_time is not None:
            return {"status": "Fault detected", "fault_start": mn_time, "fault_end": mx_time}
        else:
            return {"status": "No fault detected", "fault_start": None, "fault_end": None}

    except Exception as e:
        return {"error": str(e)}




@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return {"error": "An unexpected error occurred"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return {"error": "Validation error"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
