# app/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from app.detector import FlowAnomalyDetector
from app.ip_enrichment import enrich_dataframe
import io

app = FastAPI()
detector = FlowAnomalyDetector()

@app.get("/test")
async def test():
    return {"message": "API is working"}

@app.post("/detect")
async def detect_anomalies(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to read CSV: {e}"}, status_code=400)

    required = {'duration', 'bytes_sent', 'bytes_received', 'dst_ip'}
    missing = required - set(df.columns)
    if missing:
        return JSONResponse(
            content={"error": f"Missing required columns: {missing}"},
            status_code=400
        )

    try:
        result_df = detector.detect(df)
    except Exception as e:
        return JSONResponse(content={"error": f"Anomaly detection failed: {e}"}, status_code=500)

    try:
        enriched_df = enrich_dataframe(result_df)
    except Exception as e:
        return JSONResponse(content={"error": f"IP enrichment failed: {e}"}, status_code=500)

    results = enriched_df.to_dict(orient='records')
    return {"results": results}
