from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()
db_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(db_connection_string)

def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        # Convert each row to a dictionary using _mapping
        jobs = [row._mapping for row in result]
        return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :val"),
            {"val": id}  # Use a dictionary for parameters
        )
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            # Convert to dictionary using _mapping
            return rows[0]._mapping

def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("""
            INSERT INTO applications 
            (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) 
            VALUES 
            (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)
        """)
        # Create a parameters dictionary
        params = {
            "job_id": job_id,
            "full_name": data['full_name'],
            "email": data['email'],
            "linkedin_url": data['linkedin_url'],
            "education": data['education'],
            "work_experience": data['work_experience'],
            "resume_url": data['resume_url']
        }
        conn.execute(query, params)
        conn.commit()