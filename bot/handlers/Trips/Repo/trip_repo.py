from Repository.repository import Repository

class TripRepository(Repository):
    tables = "trips"
    init_msg = """
                DO $$ BEGIN 
                    CREATE TYPE location AS (name TEXT, time_arrival TEXT, time_departure TEXT); 
                EXCEPTION 
                    WHEN duplicate_object THEN null; 
                END $$; 
                CREATE TABLE IF NOT EXISTS trips (id SERIAL PRIMARY KEY, name TEXT, description TEXT, locations location[], entity_id TEXT, UNIQUE(name))
            """
    
