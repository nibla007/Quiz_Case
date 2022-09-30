import os
from questions import quiz


def quiz_program():
    score = 0
    num_questions = len(quiz)
    for dictionary in quiz:
        for question, answer in dictionary.items():
            print(question)
            user_answer = input("Enter Answer: ")
            check = check_answer(answer, user_answer)
            if check:
                score += 1
    return score, num_questions


def check_answer(answer, user_answer):
    if answer.lower().strip() == user_answer.lower().strip():
        print("Correct!\n")
        return True
    else:
        print(f"Wrong! Correct answer: {answer}\n")
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
    results, total_questions = quiz_program()
    print(f"You got {results} / {total_questions}")


if __name__ == '__main__':
    main()
