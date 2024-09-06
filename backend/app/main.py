import uvicorn

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import time

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000", 
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Load the model
# with open("app/churn_model.pkl", "rb") as f:
#     model = pickle.load(f)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # df = read_data()
    # model.predict(df)
    # data = prepare_data_fo_plot_from_original_dataset()
    # predict = prepare_data_fo_plot_from_predict()
    # metrics = extract_metrics(predict)
    
    time.sleep(3)
    return {"filename": file.filename, "message": "CSV file received successfully!"
     , 
    "plotdata": {
        "data" : {
            "x": ['2013-10-04 22:23:00', '2013-10-05 22:23:00', '2013-10-06 22:23:00'],
            "y": [1, 3, 6],
            "type": 'scatter',
            "marker": {"color": 'blue'}
        },
        "prediction" : {
            "x": ['2013-10-06 22:23:00', '2013-10-07 22:23:00', '2013-10-08 22:23:00', '2013-10-09 22:23:00'],
            "y": [6, 5, 3, 6],
            "type": 'scatter',
            "marker": {"color": 'red'}
        }
    },
    "metrics": {
        "accuracy": 0.87,
        "recall": 0.7
    }
    }

@app.get("/")
async def root():
    return {"message": "Hello World"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    