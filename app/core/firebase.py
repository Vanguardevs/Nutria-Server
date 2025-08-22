from firebase_admin import credentials, initialize_app, db
import firebase_admin
import os

# Verifica se o Firebase já foi inicializado
if not firebase_admin._apps:
    cred = credentials.Certificate(os.path.join(os.path.dirname(__file__), "../../firebase/nutria.json"))
    # cred = credentials.Certificate("/etc/secrets/nutria.json")
    initialize_app(cred, {
        'databaseURL': 'https://nutria-eafaa-default-rtdb.firebaseio.com/'
    })
