from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class Note(BaseModel):
    title: str
    content: str

# Create
@app.post("/notes")
def create_note(note: Note):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (note.title, note.content))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return {"id": note_id, "title": note.title, "content": note.content}

# Get all
@app.get("/notes")
def get_notes():
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "title": r[1], "content": r[2]} for r in rows]

# Get one
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "title": row[1], "content": row[2]}
    return {"error": "Note not found"}

# Update
@app.put("/notes/{note_id}")
def update_note(note_id: int, note: Note):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ? WHERE id = ?", (note.title, note.content, note_id))
    conn.commit()
    conn.close()
    return {"id": note_id, "title": note.title, "content": note.content}

# Delete
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = sqlite3.connect("journal.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return {"message": "Deleted"}
