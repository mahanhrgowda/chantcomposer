
# 🌐 Bhāva Classifier API using FastAPI
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import numpy as np
import random

app = FastAPI()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    dummy_audio = np.frombuffer(contents, dtype=np.int16)
    # Placeholder model
    classes = ["Śāntiḥ", "Bhaktiḥ", "Premaḥ", "Vīraḥ", "Karunā", "Raudraḥ", "Adbhutam", "Hāsyaḥ", "Bhayānakaḥ", "Bībhatsaḥ"]
    return JSONResponse({"predicted_bhava": random.choice(classes)})
