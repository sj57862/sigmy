from pydantic import BaseModel

class TokenPydant(BaseModel):
    accessToken:str
    refreshToken:str
    tokenType:str