import os
from questions import quiz


def check_answer(que, ans):
    if quiz[que]['answer'].lower() == ans.lower():
        print(f"Correct Answer!")
        return True
    else:
        print(f"Wrong Answer, try again")
        return False


def intro_message():
    print("Welcome to my python quiz!\n"
          "In this quiz you'll answer questions about python and it's syntax\n")
    user = input("Before we start, what's your name? ")
    input(f"Good luck {user}!\n"
          "Press enter to begin the quiz\n")
    os.system('cls')


def main():
    intro_message()
    for question in quiz:
        print(quiz[question]['question'])
        answer = input("Enter Answer: ")
        check_answer(question, answer)


if __name__ == '__main__':
    main()
