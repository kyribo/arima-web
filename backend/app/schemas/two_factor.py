from pydantic import BaseModel

class TwoFactorSetupResponse(BaseModel):
    secret: str
    qr_code_url: str

class TwoFactorEnableRequest(BaseModel):
    token: str

class TwoFactorVerifyRequest(BaseModel):
    token: str
