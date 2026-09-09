import os
import json
import datetime

from app.chat.chat import add_message


def create_user(
    username: str,
    password: str,
    full_name: str,
    city: str,
    date_of_birth: datetime.datetime,
) -> dict | None:
    # Create the user
    user = {
        "id": 0,
        "username": username,
        "password": password,  # Passwords must be encrypted
        "full_name": full_name,
        "city": city,
        "date_of_birth": str(date_of_birth),
        "created_at": str(datetime.datetime.now()),
    }

    if os.path.exists("app/user/users.json"):
        with open("app/user/users.json", "r") as file:
            # Trying to read a file and check if it contains text
            try:
                data = json.load(file)
                # Check the duplicate user
                for existed_user in data["users"]:
                    if existed_user["username"] == username:
                        return None  # Here we can throw a custom error exception and then handle that error
            except json.JSONDecodeError:
                data = {"users": []}
    else:
        data = {"users": []}

    # Add the user ID
    user["id"] = len(data["users"]) + 1

    data["users"].append(user)

    # Writing data to a json file
    with open("app/user/users.json", "w") as file:
        json.dump(data, file)

    return user


def update_user(
    # For better data validation, it is better to use pydantic or other dataclass libraries
    user_id: int,
    username: str | None = None,
    password: str | None = None,
    full_name: str | None = None,
    city: str | None = None,
    date_of_birth: str | None = None,
) -> dict | None:
    # Search the user
    with open("app/user/users.json", "r") as file:
        data = json.load(file)

    # Update the user
    for user in data["users"]:
        if user["id"] == user_id:
            updates = {
                "username": username,
                "password": password,
                "full_name": full_name,
                "city": city,
                "date_of_birth": date_of_birth,
            }

            for key, value in updates.items():
                if value is not None:
                    user[key] = value

            # Writing data to a json file
            with open("app/user/users.json", "w") as file:
                json.dump(data, file)

            return user
    return None  # Here we can throw a custom error exception and then handle that error


def get_user(username: str) -> dict | None:
    with open("app/user/users.json", "r") as file:
        users_json = json.load(file)
        for user in users_json["users"]:
            if user["username"] == username:
                return user
        return None  # Here we can throw a custom error exception and then handle that error


def send_message(chat_id: int, user_id: int, message: str) -> None:
    # If
    new_message = {
        "username": get_user(user_id)["username"],
        "text": message,
        "date": str(datetime.datetime.now()),
        "is-operator": False,
    }
    add_message(chat_id, new_message)
