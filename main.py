from app import utils


def main():
    user_choose = input("User/Operator (u/o) or simulate process work (s): ")
    if user_choose == "u":
        utils.user_choice()
    elif user_choose == "o":
        utils.operator_choice()
    elif user_choose == "s":
        utils.simulate_work(101)
    else:
        print("Invalid input")


if __name__ == "__main__":
    main()
