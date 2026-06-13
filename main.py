from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Temporary storage (in memory)
notes = []
counter = {"id": 1}

# Note structure
class Note(BaseModel):
    title: str
    content: str

# Create a note
@app.post("/notes")
def create_note(note: Note):
    new_note = {
        "id": counter["id"],
        "title": note.title,
        "content": note.content
    }
    notes.append(new_note)
    counter["id"] += 1
    return new_note

# Get all notes
@app.get("/notes")
def get_notes():
    return notes

# Get one note
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            return note
    return {"error": "Note not found"}

# Delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            return {"message": "Deleted"}
    return {"error": "Note not found"}
