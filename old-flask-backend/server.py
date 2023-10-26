from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
from algorithms.main import FaultDetection
from algorithms.main import EventClassification
from algorithms.main2 import FaultDetectionV1
from algorithms.main2 import EventClassificationV1
from typing import List
from fastapi import HTTPException

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class WindowSettings(BaseModel):
    windowSize: float = None
    sd_th: float = None

class EventSettings(BaseModel):
    time: List[float]
    data: List[float]
    thresholdValues: List[float]

@app.post("/")
async def index():
    return {"message": "Welcome to the API"}


@app.post("/v2/classify-event")
async def classify_event_data(event_settings: EventSettings):
    if not event_settings.time or not event_settings.data or not event_settings.thresholdValues:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    eventClassification = EventClassification(event_settings)
    return eventClassification.classifyEvents()

@app.post("/v2/detect-event")
async def detect_event(event_settings: EventSettings):
    if not event_settings.time or not event_settings.data:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    faultDetection = FaultDetection()
    res = faultDetection.getFault(
        [event_settings.data, event_settings.time],
        float(event_settings.windowSize),
        float(event_settings.sd_th),
    )
    if res:
        data_freq, data_rocof, data_time = res
        return {"fault": True, "freq": data_freq, "time": data_time, "rocof": data_rocof}
    return {"fault": False}

@app.post("/v2/detect-islanding-event")
async def detect_islanding_event(event_settings: EventSettings):
    if not event_settings.time or not event_settings.data or not event_settings.thresholdValues:
        raise HTTPException(status_code=400, detail="Bad request from the client")
    eventClassification = EventClassification(event_settings)
    res = eventClassification.islandingEvent()
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
