from ninja import Schema, Field



class InjectRemoteThreadResults(Schema):
    shellcode: str = Field(..., description="Shellcode in base64 decoded.")
    pid: int = Field(..., description="Process id of the target process.")
