import os
import json
import datetime


def create_user(
    username: str,
    password: str,
    full_name: str,
    city: str,
    date_of_birth: datetime.datetime,
) -> None:
    # Create user
    user = {
        "id": 0,
        "username": username,
        "password": password,  # Passwords must be encrypted
        "full_name": full_name,
        "city": city,
        "date_of_birth": str(date_of_birth),
    }

    if os.path.exists("app/user/users.json"):
        with open("app/user/users.json", "r") as file:
            # Trying to read a file and check if it contains text
            try:
                data = json.load(file)
                # Check duplicate user
                for existed_user in data["users"]:
                    if existed_user["username"] == username:
                        print("User already exists")
                        return
            except json.JSONDecodeError:
                data = {"users": []}
    else:
        data = {"users": []}

    # Add id for user
    user["id"] = len(data["users"]) + 1

    data["users"].append(user)

    # Writing data to a json file
    with open("app/user/users.json", "w") as file:
        json.dump(data, file)


def update_user(
    # For better data validation, it is better to use pydantic or other dataclass libraries
    username: str,
    full_name: str | None = None,
    city: str | None = None,
    date_of_birth: str | None = None,
) -> dict | None:
    # Search user
    with open("app/user/users.json", "r") as file:
        data = json.load(file)

    # Update user
    for user in data["users"]:
        if user["username"] == username:
            if full_name is not None:
                user["full_name"] = full_name
            if city is not None:
                user["city"] = city
            if date_of_birth is not None:
                user["date_of_birth"] = date_of_birth

            # Writing data to a json file
            with open("app/user/users.json", "w") as file:
                json.dump(data, file)

            return user
    return None


def get_user(user_id: int) -> dict | None:
    with open("app/user/users.json", "r") as file:
        users_json = json.load(file)
        for user in users_json["users"]:
            if user["id"] == user_id:
                return user
        return None


def send_message(username: str, message: str) -> None: ...
