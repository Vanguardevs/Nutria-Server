from pydantic import BaseModel
import firebase_admin
from core.firebase import firebase_admin, db

admin = firebase_admin

def ver_dados():
    ref = db.reference("users")
    return ref.get()