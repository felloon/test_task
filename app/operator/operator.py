import os
import json
import datetime
import random

from app.chat.chat import (
    add_message,
    change_operator_assignment_status,
    close_chat,
    get_chat_messages,
)


def create_operator(
    username: str,
    password: str,
    full_name: str,
    city: str,
    job_title: str,
    work_experience: str,
    date_of_birth: datetime.datetime,
) -> dict | None:
    # Create the operator
    operator = {
        "id": None,
        "username": username,
        "password": password,  # Passwords must be encrypted
        "full_name": full_name,
        "city": city,
        "job_title": job_title,
        "work_experience": work_experience,
        "date_of_birth": str(date_of_birth),
        "created_at": str(datetime.datetime.now()),
        "assigned_chat": False,
        "assigned_chat_id": None,
    }

    if os.path.exists("app/operator/operators.json"):
        with open("app/operator/operators.json", "r") as file:
            # Trying to read a file and check if it contains text
            try:
                data = json.load(file)
                # Check the duplicate operator
                for existed_operator in data["operators"]:
                    if existed_operator["username"] == username:
                        return None
            except json.JSONDecodeError:
                data = {"operators": []}
    else:
        data = {"operators": []}

    # Add the operator ID
    operator["id"] = len(data["operators"]) + 1

    data["operators"].append(operator)

    # Writing data to a json file
    with open("app/operator/operators.json", "w") as file:
        json.dump(data, file)

    return operator


def update_operator(
    # For better data validation, it's better to use pydantic or other dataclass libraries
    operator_id: int,
    username: str | None = None,
    password: str | None = None,
    full_name: str | None = None,
    city: str | None = None,
    job_title: str | None = None,
    work_experience: str | None = None,
    date_of_birth: str | None = None,
    assigned_chat: bool = False,
    assigned_chat_id: int | None = None,
) -> dict | None:
    # Search the operator
    with open("app/operator/operators.json", "r") as file:
        data = json.load(file)

    # Update the operator
    for operator in data["operators"]:
        if operator["id"] == operator_id:
            updates = {
                "username": username,
                "password": password,
                "full_name": full_name,
                "city": city,
                "job_title": job_title,
                "work_experience": work_experience,
                "date_of_birth": date_of_birth,
                "assigned_chat": assigned_chat,
                "assigned_chat_id": assigned_chat_id,
            }

            for key, value in updates.items():
                if value is not None:
                    operator[key] = value

            # Writing data to a json file
            with open("app/operator/operators.json", "w") as file:
                json.dump(data, file)

            return operator
    return None  # Here we can throw a custom error exception and then handle that error


def get_operator(operator_id: int) -> dict | None:
    with open("app/operator/operators.json", "r") as file:
        operators_json = json.load(file)
        for operator in operators_json["users"]:
            if operator["id"] == operator_id:
                return operator
        return None  # Here we can throw a custom error exception and then handle that error


def send_message_to_client(chat_id: int, username: str) -> str | None:
    # The operator responds to the user's message and closes the chat after
    with open("app/operator/operators.json", "r") as file:
        data = json.load(file)

    # Check that a chat has been assigned to the operator and that there is a user's message
    for operator in data["operators"]:
        if operator["username"] == username and operator["assigned_chat"] is True:
            # Displays all messages from the chat
            chat_messages = get_chat_messages(chat_id)
            if chat_messages is None:
                return "Chat not found"  # Here we can throw a custom error exception and then handle that error
            for message in chat_messages:
                print(
                    f"User: {message['username']}\nMessage: {message['text']}\nDate: {message['date']}\n"
                )
            response = input()  # Operator's response
            message = {
                "username": username,
                "text": response,
                "date": str(datetime.datetime.now()),
                "is-operator": True,
            }
            # Adds the message to the chat and change the chat's and operator's statuses
            add_message(chat_id, message)
            change_operator_assignment_status(chat_id, False)
            operator["assigned_chat"] = False
            operator["assigned_chat_id"] = None
            operator_response = input("Do you want to close the chat? (y/n): ")
            if operator_response == "y":
                close_chat(chat_id)
            elif operator_response == "n":
                return "Operator sent reply successfully"
            else:
                return "Incorrect input"
    return "No chat have been assigned yet"  # Here we can throw a custom error exception and then handle that error


def choose_operator() -> dict | None:
    # Choose an operator who hasn't assigned to the chat (Func not good, there are some trouble, but in this case it's ok)
    with open("app/operator/operators.json", "r") as file:
        operators_json = json.load(file)

    # To avoid recursion and an infinity search, I added few attempts
    for i in range(200):
        operator = random.choice(operators_json["operators"])
        if operator["assigned_chat"] is False:
            return operator

    return None  # Here we can throw a custom error exception and then handle that error


def assign_chat(chat_id: int) -> dict | str:
    # Assigns the chat to the operator
    operator = choose_operator()
    if operator is None:
        return "No active operators"  # Here we can throw a custom error exception and then handle that error

    operator["assigned_chat"] = True
    operator["assigned_chat_id"] = chat_id

    update_operator(
        operator_id=operator["id"],
        assigned_chat=operator["assigned_chat"],
        assigned_chat_id=operator["assigned_chat_id"],
    )

    # Change status of the chat
    change_operator_assignment_status(chat_id, True)

    return operator
