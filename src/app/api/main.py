from fastapi import FastAPI, HTTPException

from src.parser.main import parse
from src.app.api.models import ConvertResponse, ConvertBody

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the API!"}


@app.post("/convert")
async def convert(request: ConvertBody):

    if request.convert_lang != "json":
        raise HTTPException(status_code=500, detail="Only JSON conversion is available.")

    result, valid, message = parse(request.data)

    return ConvertResponse(
        result=result,
        valid=valid,
        message=message
    )

