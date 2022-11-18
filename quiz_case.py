import requests
import random
import json

url = "https://bjornkjellgren.se/quiz/v2/questions"


def check_answer(user_input, answers):
    user_choice = answers[user_input - 1]
    all_answers = []
    for answer in answers:
        if answer.get("correct"):
            all_answers.append(answer.get("answer"))

    the_correct_answers = ' eller '.join(all_answers)

    if user_choice.get("correct"):
        return "Rätt!\n", 1, the_correct_answers, True
    return f"Fel! Rätt svar är: {the_correct_answers}\n", 0, the_correct_answers, False


def save_wrong_answers(f, s):
    return f, s


def procent(a, b):
    if b == 0:
        return 0
    return 100 * a / b


def post_data(i, c):
    payload = json.dumps({"id": i, "correct": c})
    requests.post(url, data=payload)


def quiz_program():
    wrong_answers = []
    r = requests.get(url)
    r_dict = r.json()
    all_questions = r_dict.get("questions")
    random_questions = random.sample(all_questions, k=len(all_questions))[:10]
    score = 0
    user_input = None
    print(f"Slumpar fram {len(random_questions)} av {len(all_questions)} frågor.\n")

    for question_id, question in enumerate(random_questions, start=1):
        prompt = question.get("prompt")
        times_asked = int(question['times_asked'])
        times_correct = int(question['times_correct'])
        print(f"Fråga {question_id}.[{int(procent(times_correct, times_asked))}% har svarat rätt]\n{prompt}")

        all_answers = question.get("answers")
        random.shuffle(all_answers)

        for count, answer in enumerate(all_answers, start=1):
            print(f"{count}. {answer['answer']}")
        while True:
            try:
                user_input = int(input("\nDitt svar: "))
            except ValueError:
                print("Ogiltigt värde")
                continue
            if 1 <= user_input <= len(all_answers):
                break
            else:
                print(f'\nOgiltigt svar, svara med 1 till {len(all_answers)}')

        result, point, correct_answers, correct_bool = check_answer(user_input, all_answers)
        post_data(question.get("id"), correct_bool)
        if not correct_bool:
            wrong_answers.append(save_wrong_answers(prompt, correct_answers))
        print(result)
        score += point

    print(f"\n***RESULTAT***\nDu fick {score} rätt av {len(random_questions)} möjliga")
    if wrong_answers:
        print(f"Du svarade fel på dessa frågor:")
        for question, answer in wrong_answers:
            print(f"-{question}")
            print(f"Rätt svar: {answer}")


def main():
    quiz_program()


if __name__ == '__main__':
    main()
