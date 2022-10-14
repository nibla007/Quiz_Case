import requests
import random


def check_answer(user_input, answers):
    user_choice = answers[user_input - 1]
    the_correct_answer = "not found"
    for answer in answers:
        if answer.get("correct"):
            the_correct_answer = answer.get("answer")

    if user_choice.get("correct"):
        return "Rätt!\n", 1
    return f"Fel! Rätt svar är: {the_correct_answer}\n", 0


def quiz_program():
    url = "https://bjornkjellgren.se/quiz/v1/questions"
    r = requests.get(url)
    r_dict = r.json()
    score = 0

    for question in r_dict["questions"]:
        question_id = question.get("id")
        prompt = question.get("prompt")
        print(f"Fråga {question_id}. {prompt}")

        all_answers = question.get("answers")
        random.shuffle(all_answers)

        for count, all_answers in enumerate(question.get("answers"), start=1):
            answer = all_answers.get("answer")
            print(f"{count}. {answer}")
        user_input = int(input("Ditt svar: "))
        result, point = check_answer(user_input, question.get("answers"))
        print(result)
        score += point

    print(f"\n***RESULTAT***\nDu fick {score} rätt av {len(r_dict.get('questions'))} möjliga")


def main():
    quiz_program()


if __name__ == '__main__':
    main()
