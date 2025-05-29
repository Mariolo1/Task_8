import sqlite3

class Database:
    def __init__(self, db_name="jobs.db"):
        self.db_name = db_name
        self._setup_database()

    def _setup_database(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    description TEXT,
                    add_info TEXT,
                    company_location TEXT,
                    salary TEXT,
                    tech_stack TEXT
                )
            ''')
            conn.commit()

    def save_to_database(self, job_data):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO jobs (url, title, description, add_info, company_location, salary, tech_stack)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data["url"],
                job_data["title"],
                job_data["description"],
                job_data["add_info"],
                job_data["company_location"],
                job_data["salary"],
                job_data["tech_stack"]
            ))
            conn.commit()
