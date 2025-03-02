from Repository.repository import Repository

class NoteRepository(Repository):
    tables = "notes"
    init_msg = """
                CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, id_trip INTEGER REFERENCES trips(id) ON DELETE CASCADE, files TEXT[], files_names TEXT[], note_text TEXT, unique_id_trip INTEGER, UNIQUE(unique_id_trip));
                """