from pydantic import BaseModel


class Note(BaseModel):
    title: str
    note: str
    date: str
