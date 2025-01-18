from ...services.view_base import ApiRouteV2
from typing import Dict, Optional
from application.views.api.Schemas.general import SuccessBase
from ninja import Schema, Field
from pydantic import field_validator


class getsomthingin(Schema):
    test: str = Field(default="123", description="An optional test string")
    test2: str = Field(..., description="A required string that must be alphabetic")

    @field_validator("test2")
    def validate_test2(cls, value: str) -> str:
        if not value == "123":
            raise ValueError("The field 'test2' must be 123.")
        return value





class getsomthingout(Schema):
    arg1: str
    arg2: str
    arg3: Optional[int] = None
    
    

class TestApi(ApiRouteV2):

    def __init__(self):
        super().__init__(tags=["Test"])
        self.register_routes()

    async def getsomthing(self, request, payload:getsomthingin, *args, **kwargs):
        return getsomthingout(arg1="blabla", arg2="bla")

    async def get_item(self, request, item_id:int):
        return getsomthingout(arg1="blabla", arg2="bla")

    def register_routes(self):
        self.register_route(
            path="/{item_id}",
            methods=["GET"], 
            view_func=self.get_item,
            response={200: getsomthingout},
            summary="Fuck you",
            permissions_req=["application.agent_add"]
        )
        self.register_route(
            path="/", 
            methods=["POST"], 
            view_func=self.getsomthing,
            response={200: getsomthingout}
        )
