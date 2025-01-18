from ninja import Schema

class SuccessBase(Schema):
    detail: str

class DeletedSuccessfully(SuccessBase):
    # default value for the detail field:
    detail: str = "Deleted successfully"

class EditedSuccessfully(SuccessBase):
    detail: str = "Edited successfully"

class CreatedSuccessfully(SuccessBase):
    detail: str = "Created successfully"