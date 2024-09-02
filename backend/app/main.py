import uvicorn

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

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
    # Read the CSV file into a DataFrame
    # df = pd.read_csv(file.file)
    
    # Here you could add logic to make predictions using the loaded model
    # predictions = model.predict(df)
    
    # For now, just confirm the file was received
    return {"filename": file.filename, "message": "CSV file received successfully!"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    