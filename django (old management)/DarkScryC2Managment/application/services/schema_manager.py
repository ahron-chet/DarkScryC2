from pydantic import BaseModel, model_validator


class SchemaManager(BaseModel):
    # db_manager: DBManager = Field(default_factory=DBManager, exclude=True)
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"

    # @staticmethod
    # def get_db(values:ValidationInfo) -> DBManager:
    #     return values.data.get("db_manager")
    
    @model_validator(mode='before')
    def check_extra_fields(cls, values):
        valid_fields = set(cls.model_fields.keys())
        incoming_fields = set(values.keys())

        extra_fields = incoming_fields - valid_fields

        if extra_fields:
            raise ValueError(f"Extra fields are not allowed: {extra_fields}")
        return values