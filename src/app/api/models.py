from pydantic import BaseModel


class ConvertBody(BaseModel):
    data: str
    convert_lang: str


class ConvertResponse(BaseModel):
    result: str
    valid: bool
    message: str
