from pydantic import BaseModel, ConfigDict


class MyBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class TypesRead(MyBaseModel):
    id: int
    name: str


class TypesCreate(MyBaseModel):
    name: str
