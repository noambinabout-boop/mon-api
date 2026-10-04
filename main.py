from fastapi import FastAPI, Request, HTTPException
import os
import hmac
import hashlib
import subprocess
import json

from dataBaseManagment.notesDataBase import NotesDataBase
from models import Note


app = FastAPI()


@app.get("/health")
def health():
    return {"Status": "ok", "version": "2"}


@app.post("/webhook")
async def webHooks(request: Request):
    corps = await request.body()

    signature = request.headers.get("X-Hub-Signature-256")
    if signature is None:
        raise HTTPException(status_code=401, detail="Signature absente")

    strip_signature = signature.removeprefix("sha256=")
    cle_webhook = os.environ["WEBHOOK_SECRET"]
    my_key_digested = hmac.new(cle_webhook.encode("utf-8"), corps, hashlib.sha256).hexdigest()

    if hmac.compare_digest(my_key_digested, strip_signature):

        json_request = json.loads(corps.decode("utf-8"))
        if request.headers.get("X-GitHub-Event") != "push":
            return {"Message": "C'est un ping"}
    
        if json_request["ref"] != "refs/heads/main":
            return {"Message": "Pas la bonne branche"}

        subprocess.run("sudo -n /usr/bin/systemctl start --no-block mon-api-deploy.service".split(" "))
        return {"Message": "accepté, traitement en cours"}
    
    raise HTTPException(status_code=401, detail="Les signatures ne sont pas les mêmes")


@app.get("/db/note/{id}")
def get_notes_id(id: int):
    notes_db = NotesDataBase("notes.db")
    result = notes_db.get_notes_with_id()
    if result != []:
        return {"Note": result[0][1]}
    raise HTTPException(status_code="404", detail="Not found")


@app.post("/db/note")
def add_note(note: Note):
    notes_db = NotesDataBase("notes.db")
    result = notes_db.insert_new_note(note.Note.title, note.Note.note, note.Note.date)
    if result:
        return {"Message": "Tout s'est bien passé !"}
    raise HTTPException(status_code=401, detail="Erreur lors de la création de la note")
