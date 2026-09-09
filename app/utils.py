import datetime
import json
import random

from app.chat import chat
from app.user import user
from app.operator import operator


def user_choice() -> None:
    clear_json_files()
    main_user = user.create_user(
        random.randint(1, 1000),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        datetime.datetime.now(),
    )
    operator.create_operator(
        random.randint(1, 1000),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        datetime.datetime.now(),
    )
    user_message = input("Your message: ")
    chat_id = chat.create_chat(
        main_user["id"],
        main_user["username"],
        user_message,
        datetime.datetime.now(),
    )
    main_operator = operator.assign_chat(chat_id)
    message = {
        "username": main_operator["username"],
        "text": "Ok",
        "date": str(datetime.datetime.now()),
        "is-operator": True,
    }
    print(
        f"User: {message['username']}\nMessage: {message['text']}\nDate: {message['date']}\n"
    )
    chat.add_message(chat_id, message)
    chat.change_operator_assignment_status(chat_id, False)
    main_operator["assigned_chat"] = False
    main_operator["assigned_chat_id"] = None
    chat.close_chat(chat_id)
    user_csat = input("How would you rate this answer? (1-5): ")
    if user_csat in range(1, 6):
        chat.set_csat(chat_id, int(user_csat))


def operator_choice() -> None:
    clear_json_files()
    main_operator = operator.create_operator(
        random.randint(1, 1000),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        datetime.datetime.now(),
    )
    chat_id = create_test_message(main_operator["id"])
    operator.send_message_to_client(chat_id, main_operator["username"])


def simulate_work(times: int) -> None:
    clear_json_files()
    for _ in range(times):
        main_user = None
        while main_user is None:
            main_user = user.create_user(
                random.randint(1, 1000),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                datetime.datetime.now(),
            )
        main_operator = None
        while main_operator is None:
            main_operator = operator.create_operator(
                random.randint(1, 1000),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                random.randint(1, 100),
                datetime.datetime.now(),
            )
        chat_id = chat.create_chat(
            main_user["id"],
            main_user["username"],
            f"Try: {times}",
            datetime.datetime.now(),
        )
        operator.assign_chat(chat_id)
        attempt = random.randint(1, 2)
        # Try to send the operator's message
        if attempt == 1:
            message = {
                "username": main_operator["username"],
                "text": "Ok",
                "date": str(datetime.datetime.now()),
                "is-operator": True,
            }
            chat.add_message(chat_id, message)
            chat.change_operator_assignment_status(chat_id, False)
            main_operator["assigned_chat"] = False
            main_operator["assigned_chat_id"] = None
            attempt = random.randint(1, 2)
            # Try to close the chat
            if attempt == 1:
                chat.close_chat(chat_id)
                attempt = random.randint(1, 2)
                # Try to set the CSAT
                if attempt == 1:
                    chat.set_csat(chat_id, random.randint(1, 5))
                    print("A chat with CSAT has been created")
                else:
                    print("A chat without CSAT has been created")
                    continue
            else:
                print("An open chat with operator's answer has been created")
                continue
        else:
            print("An open chat without operator's answer has been created")
            continue


def create_test_message(operator_id: int) -> int:
    main_user = user.create_user(
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        random.randint(1, 100),
        datetime.datetime.now(),
    )
    chat_id = chat.create_chat(
        main_user["id"],
        main_user["username"],
        "Hello, my order is not arrived",
        datetime.datetime.now(),
    )
    operator.update_operator(
        operator_id=operator_id,
        assigned_chat=True,
        assigned_chat_id=chat_id,
    )
    return chat_id


def clear_json_files() -> None:
    open("app/chat/chats.json", "w").close()
    open("app/operator/operators.json", "w").close()
    open("app/user/users.json", "w").close()
