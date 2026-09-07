import os
import json
import datetime

from app.user.user import get_user


def create_chat(user_id: int, message: str, date: datetime.datetime) -> str | None:
    # Check user
    if get_user(user_id) is None:
        return "User not found"

    # Create a chat if a user send first message
    chat = {
        "id": 0,
        "user_id": user_id,
        "messages": [
            {
                "username": get_user(user_id)["username"],
                "text": message,
                "date": str(date),
                "is-operator": False,
            }
        ],
        "csat": 0,
        "active": True,
    }

    if os.path.exists("app/chat/chats.json"):
        with open("app/chat/chats.json", "r") as file:
            # Trying to read a file and check if it contains text
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"chats": []}
    else:
        data = {"chats": []}

    # Add id for chat
    chat["id"] = len(data["chats"]) + 1

    data["chats"].append(chat)

    # Writing data to a json file
    with open("app/chat/chats.json", "w") as file:
        json.dump(data, file)

    return "Chat created"


def add_message(user_id: int, message: str, date: datetime.datetime) -> str | None:
    # Get active chat id by user
    chat_id = get_active_id_chat_by_user(user_id)
    if chat_id is None:
        return "Chat not found"

    # Create new message
    new_message = {
        "username": get_user(user_id)["username"],
        "text": message,
        "date": str(date),
        "is-operator": False,
    }

    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    # Adding message in active chat
    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["messages"].append(new_message)

    with open("app/chat/chats.json", "w") as file:
        json.dump(data, file)

    return "Message added"


def get_active_id_chat_by_user(user_id: int) -> int | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == user_id and chat["active"] == True:
            return chat["id"]
    return None


def get_all_chats_by_user(user_id: int) -> list[dict]:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    chats = []

    for chat in data["chats"]:
        if chat["user_id"] == user_id:
            chats.append(chat)

    return chats


def set_csat(chat_id: int, csat: int) -> str | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["csat"] = csat

            with open("app/chat/chats.json", "w") as file:
                json.dump(data, file)

            return "CSAT set"
    return None
