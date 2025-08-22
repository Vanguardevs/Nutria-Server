from fastapi import FastAPI
from app.api.v1.endpoints.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/v1")

@app.get('/')
def main():
    return {"message": "ON"}