from notes.models import Note


def map_note_to_dto(note: Note) -> dict:
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "user_id": note.user_id,
    }
