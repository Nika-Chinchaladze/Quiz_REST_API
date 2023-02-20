from pydantic import BaseModel


class AddModel(BaseModel):
    question: str
    answer: str
    category: str
    level: str
    wrong1: str
    wrong2: str
    wrong3: str


class UpdateModel(BaseModel):
    api_key: str
    field_name: str
    new_value: str


class ChangeModel(BaseModel):
    question: str
    answer: str
    category: str
    level: str
    wrong1: str
    wrong2: str
    wrong3: str
    api_key: str
