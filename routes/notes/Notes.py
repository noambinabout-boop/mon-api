from fastapi import APIRouter, HTTPException
from dataBaseManagment.notesDataBase import NotesDataBase
from models.Note import Note


router = APIRouter(prefix="/db/note")

@router.get("/")
def get_all_notes():
    notes_db = NotesDataBase("notes.db")
    result = notes_db.get_all_notes()
    return result


@router.get("/id/{id}")
def get_notes_id(id: int):
    notes_db = NotesDataBase("notes.db")
    result = notes_db.get_notes_with_id(id)
    if result != []:
        return {"Note": result[0][1:]}
    raise HTTPException(status_code=404, detail="Not found")


@router.get("/title/{title}")
def get_note_title(title: str):
    notes_db = NotesDataBase("notes.db")
    result = notes_db.get_notes_with_title(title)
    if result != []:
        return {"Note": result[0][1:]}
    raise HTTPException(status_code=404, detail="Not found")


@router.post("/")
def add_note(note: Note):
    notes_db = NotesDataBase("notes.db")
    result = notes_db.insert_new_note(note.title, note.note, note.date)
    if result:
        return {"Message": "Tout s'est bien passé !"}
    raise HTTPException(status_code=500, detail="Erreur lors de la création de la note")



