from fastapi import FastAPI, UploadFile, File, Body
from services.exp_extractor import extract_text_from_pdf
from services.exp_extractor import process_experience
from typing import Optional

app = FastAPI()

# 경험 저장 및 분석 API
@app.post("/analyze/pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    content = await file.read()
    raw_text = extract_text_from_pdf(content)
    return process_experience(raw_text, is_json=False)

@app.post("/analyze/json")
async def analyze_json(data: dict = Body(...)):
    return process_experience(data, is_json=True)