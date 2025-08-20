from app.core.firebase import firebase_admin, db
from fastapi import FastAPI

app = FastAPI()

@app.get("/ver_dados")
def ver_dados():
    return db.reference("users").get()
