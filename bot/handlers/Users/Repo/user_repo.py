from Repository.repository import Repository

class UserRepository(Repository):
    tables = "users"
    init_msg = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, age TEXT, city TEXT, country TEXT, bio TEXT, name TEXT, entity_id TEXT)"