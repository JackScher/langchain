import json
from fastapi import APIRouter
from app.utils import get_answer
from app import schema as s
from app.logger import logger

assistant_router = APIRouter(
    prefix="/send",
    tags=["assistant"],
)


@assistant_router.post("/", response_model=s.Message)
def assistant(message_instance: s.Message):
    r = s.Message(message=get_answer(message_instance.message))
    logger.info("Response message received.")

    with open("app/default_messages.json", "r") as file:
        default_messages = json.load(file)
        for m in default_messages:
            if m in r.message.lower():
                logger.info("Default response message received.")
                r = s.Message(message=default_messages[m])
                return r
    return r
