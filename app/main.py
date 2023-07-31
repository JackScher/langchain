from app import schema as s
from app import app


@app.get("/", response_model=s.Message)
def root():
    r = s.Message(message="Hello")
    return r
