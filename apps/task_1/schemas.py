import re
from fastapi import HTTPException
from pydantic import BaseModel, validator

class IsValidMediaIdRequest(BaseModel):
    id: str

    @validator('id')
    def name_must_contain_space(cls, v):
        x = re.fullmatch('^[a-z0-9]{10,15}_[a-z0-9]{5,10}$', v)
        if v.isnumeric():
            raise HTTPException(status_code=422, detail="'int' is not allowed")
        if re.match(r'^-?\d+(?:\.\d+)$', v):
            raise HTTPException(status_code=422, detail="'float' is not allowed")
        if re.match('^(true|false|True|False)$', v):
            raise Exception()
        if not x:
            raise HTTPException(status_code=422, detail="Fail")
        return v

class ProcessRequest(BaseModel):
    media_id: str