import datetime

from app.user import user
from app.chat import chat


def main():
    # user.update_user("da1", "a net")
    # chat.create_chat(
    #     1, "hello, order not arrived, please help me", datetime.datetime.now()
    # )
    # chat.add_message(1, "hihi", datetime.datetime.now())
    chat.set_csat(1, 4)


if __name__ == "__main__":
    main()
