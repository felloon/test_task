import os
import json
import datetime


def create_chat(
    user_id: int, username: str, message: str, date: datetime.datetime
) -> int | None:
    # Create a chat if a user send first message
    chat = {
        "id": None,
        "user_id": user_id,
        "messages": [
            {
                "username": username,
                "id": user_id,
                "text": message,
                "date": str(date),
                "is-operator": False,
            }
        ],
        "csat": None,
        "active": True,
        "assigned_operator": False,
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

    return chat["id"]


def add_message(user_id: int, message: dict) -> str | None:
    # Get active chat id by user
    chat_id = get_active_chat_id_by_user_id(user_id)
    if chat_id is None:
        return None  # Here we can throw a custom error exception and then handle that error

    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    # Adding message in active chat
    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["messages"].append(message)

    with open("app/chat/chats.json", "w") as file:
        json.dump(data, file)

    return "Message added"


def get_all_chats() -> list[dict] | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    chats = []
    for chat in data["chats"]:
        chats.append(chat)

    return chats


def get_active_chat_id_by_user_id(user_id: int) -> int | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == user_id and chat["active"] == True:
            return chat["id"]
    return None  # Here we can throw a custom error exception and then handle that error


def get_all_chats_by_user_id(user_id: int) -> list[dict]:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    chats = []

    for chat in data["chats"]:
        if chat["user_id"] == user_id:
            chats.append(chat)

    return chats


def get_all_chats_by_operator_id(operator_id: int) -> list[dict]:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    chats = []

    for chat in data["chats"]:
        for message in chat["messages"]:
            if message["id"] == operator_id and message["is-operator"] == True:
                chats.append(chat)

    return chats


def get_chat_messages(chat_id: int) -> list[dict] | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    messages: list[dict] = []

    for chat in data["chats"]:
        if chat["id"] == chat_id and chat["active"] == True:
            for message in chat["messages"]:
                messages.append(
                    {
                        "username": message["username"],
                        "text": message["text"],
                        "date": message["date"],
                    }
                )
            return messages
    return None  # Here we can throw a custom error exception and then handle that error


def set_csat(chat_id: int, csat: int) -> str | None:
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == chat_id and chat["active"] == False:
            chat["csat"] = csat

            with open("app/chat/chats.json", "w") as file:
                json.dump(data, file)

            return "CSAT set"
        elif chat["id"] == chat_id and chat["active"] == True:
            return "Chat not closed"
    return None  # Here we can throw a custom error exception and then handle that error


def change_operator_assignment_status(chat_id: int, status: bool) -> str | None:
    # Sets the operator assign status in chat
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["assigned_operator"] = status

            with open("app/chat/chats.json", "w") as file:
                json.dump(data, file)

            if status:
                return "Operator assigned"
            else:
                return "Operator taken off from the chat"
    return None  # Here we can throw a custom error exception and then handle that error


def close_chat(chat_id: int) -> str | None:
    # Closes the active chat when operator has replied to the user's question
    with open("app/chat/chats.json", "r") as file:
        data = json.load(file)

    for chat in data["chats"]:
        if chat["id"] == chat_id:
            chat["active"] = False
            with open("app/chat/chats.json", "w") as file:
                json.dump(data, file)
            return "Chat closed"
    return None  # Here we can throw a custom error exception and then handle that error
