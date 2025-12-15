import sys
import os
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipieline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object

load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL_KEY")
if not mongo_db_url:
    raise RuntimeError("MONGODB_URL_KEY not set")

ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="./templates")

@app.get("/", tags={"authentication"})
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipline = TrainingPipieline()
        train_pipline.run_pipeline()
        return Response("Training is succesful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=final_model
        )

        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse(
            "table.html",
            {"request": request, "table": table_html}
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys)
