from pydantic import BaseModel


class PutNoteModel(BaseModel):
    update_field: str
    new_field: str